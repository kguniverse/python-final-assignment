from sanic import Sanic
from sanic.response import json
import geopandas as gpd
from shapely.geometry import shape, Point
import numpy as np
import pandas as pd
from shapely.prepared import prep

app = Sanic("server")

class Dao:
    def __init__(self):
        self.cell_size = 0.0083333333333333
        self.NODATA_value = -9999
        self.start_x = -180
        self.start_y = 90
        filepath_base = "gpw-v4-population-count-rev11_2020_30_sec_asc/gpw_v4_population_count_rev11_2020_30_sec_"
        self.grid = None
        for col in range(2):
            grid_line = None
            for row in range(4):
                filepath = filepath_base + str(col * 4 + row + 1) + ".asc"
                # grid_part = np.loadtxt(filepath, skiprows=6)
                grid_part = pd.read_csv(filepath,header=None,na_filter=False,delim_whitespace=True, skiprows=6).to_numpy()
                if grid_line is None:
                    grid_line = grid_part
                else:
                    grid_line = np.concatenate((grid_line, grid_part), axis=1)
            if grid is None:
                grid = grid_line
            else :
                grid = np.concatenate((grid, grid_line), axis=0) 
        pass

    def validate_grid(self, gjson):
        polygon = shape(gjson['features'][0]['geometry'])
        (latmin, lonmin, latmax, lonmax) =((x // self.cell_size * self.cell_size) for x in polygon.bounds)
        prep_polygon = prep(polygon)
        points = []
        for lat in np.arange(latmin, latmax, self.cell_size):
            for lon in np.arange(lonmin, lonmax, self.cell_size):
                points.append(Point((round(lat,4), round(lon,4))))
        valid_points = []
        valid_points.extend(filter(prep_polygon.contains, points))
        sum = 0
        for point in  valid_points:
            lon, lat = point.x, point.y
            local_sum = self.grid[int((self.start_y - lat) // self.cell_size)][int((lon - self.start_x) // self.cell_size)]
            if local_sum != self.NODATA_value:
                sum += int(local_sum)
        return sum

dao = Dao()

@app.post("/data")
def dataHandler(request):
    geo = request.json
    return json({'sum': dao.validate_grid(geo)})
