# pip install ortools numpy pandas plotly pulp

import numpy as np
import pandas as pd
import pulp
import plotly.express as px
import plotly.graph_objects as go

# 1) Generate synthetic “Paris” demand
np.random.seed(1)
n = 30
demand = pd.DataFrame({
    'id':     range(n),
    'lat':    np.random.uniform(48.80, 48.90, n),
    'lon':    np.random.uniform(2.25, 2.40, n),
    'weight': np.random.randint(5, 50, n)    # orders per hour
})
# Candidate sites = same centroids
sites = demand.rename(columns={'id':'site_id'})

# Haversine function
def haversine(lat1, lon1, lat2, lon2, R=6371):
    φ1, φ2 = np.radians(lat1), np.radians(lat2)
    Δφ     = φ2 - φ1
    Δλ     = np.radians(lon2 - lon1)
    a = np.sin(Δφ/2)**2 + np.cos(φ1)*np.cos(φ2)*np.sin(Δλ/2)**2
    return 2*R*np.arcsin(np.sqrt(a))

# Precompute distances
dist = {
    (i,j): haversine(demand.loc[i,'lat'], demand.loc[i,'lon'],
                     sites.loc[j,'lat'],  sites.loc[j,'lon'])
    for i in demand.id
    for j in sites.site_id
}

# ===================================================================
# FUNCTION: solve p-median for given p (PuLP version)
# ===================================================================
def solve_pmedian(p):
    # 1. Initialize Model
    prob = pulp.LpProblem("p-Median", pulp.LpMinimize)

    # 2. Define Variables
    x = pulp.LpVariable.dicts("x", sites.site_id, cat='Binary')
    y = pulp.LpVariable.dicts("y", [(i,j) for i in demand.id for j in sites.site_id], cat='Binary')

    # 3. Objective Function
    prob += pulp.lpSum(
        demand.loc[i,'weight'] * dist[(i,j)] * y[(i,j)]
        for i in demand.id for j in sites.site_id
    )

    # 4. Constraints
    # Exactly p facilities open
    prob += pulp.lpSum(x[j] for j in sites.site_id) == p

    # Assignment and linking constraints
    for i in demand.id:
        # Each demand point must be assigned to exactly one site
        prob += pulp.lpSum(y[(i,j)] for j in sites.site_id) == 1
        for j in sites.site_id:
            # A demand point can only be assigned to an open site
            prob += y[(i,j)] <= x[j]

    # 5. Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=0)) # msg=0 suppresses solver output

    # 6. Get Results
    obj = pulp.value(prob.objective)
    opened = [j for j in sites.site_id if x[j].varValue > 0.5]
    return obj, opened
# ===================================================================

# 2) Sweep p = 1…10, record objectives
Pmax = 10
results = [solve_pmedian(p) for p in range(1, Pmax+1)]
ps      = list(range(1, Pmax+1))
objs    = [res[0] for res in results]

# Plot Objective vs p with Plotly
fig1 = px.line(x=ps, y=objs,
               labels={'x':'Number of facilities (p)',
                       'y':'Total weighted distance'},
               title='p-Median Objective vs. Number of Facilities')
fig1.show()


# 3) For p = 7, get opened sites & plot map
obj7, opened7 = results[6]  # index 6 => p=7
opened_df = sites[sites.site_id.isin(opened7)]

# Base layer: demand points
fig = px.scatter_mapbox(
    demand,
    lat="lat", lon="lon",
    size="weight",
    size_max=20,
    zoom=11,
    center={"lat":48.85, "lon":2.33},
    mapbox_style="carto-positron",
    title="Demand (size∝orders/hr) + Facilities (p=7)"
)
fig.update_traces(name="Demand", showlegend=True)

# Overlay: facilities
fig.add_trace(
    go.Scattermapbox(
        lat=opened_df["lat"],
        lon=opened_df["lon"],
        mode="markers",
        marker_size=25,
        marker_color="red",
        marker_opacity=0.9,
        name="Facilities"
    )
)

fig.show()