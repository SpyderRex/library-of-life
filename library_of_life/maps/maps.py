from typing import Optional, Dict, Any
import webbrowser
import requests
from requests.exceptions import HTTPError, Timeout, RequestException
import requests_cache
from PIL import Image
from PIL import ImageEnhance
from io import BytesIO
from .. utils import http_client as hc

base_url = "https://api.gbif.org/v2/"

class Map:
    """
    A class for interacting with the Maps API.
    
    Attributes:
        endpoint: endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                 cache_name="maps_cache", 
                 backend="sqlite", 
                 expire_after=3600,
                 save_image=True,
                 open_in_browser=False):
        self.endpoint = "map/occurrence"
        self.save_image = save_image
        self.open_in_browser = open_in_browser
                 
        if use_caching:
            requests_cache.install_cache(cache_name, backend=backend, expire_after=expire_after)
            
    def precalculated_density_tile(self, z, x, y, map_tile_format, map_projection,
                                   basis_of_record: Optional[str]=None,
                                   year: Optional[str]=None,
                                   verbose: Optional[bool]=None,
                                   binning_style: Optional[str]=None,
                                   hex_per_tile: Optional[int]=None,
                                   square_size: Optional[str]=None,
                                   map_style: Optional[str]=None,
                                   country: Optional[str]=None,
                                   taxon_key: Optional[int]=None,
                                   dataset_key: Optional[str]=None,
                                   publishing_org: Optional[str]=None,
                                   publishing_country: Optional[str]=None,
                                   network_key: Optional[str]=None):
        """
        Retrieves a tile showing occurrence locations in Mapbox Vector Tile format. Tiles contain a single layer occurrence. Features in that layer are either points (default) or polygons (if chosen). Each feature has a total value; that is the number of occurrences at that point or in the polygon. One primary search parameter is permitted, from these: taxonKey, datasetKey, country, networkKey, publishingOrg, publishingCountry. This can be combined with the parameter country, this limits the primary search to occurrences in that country.
    
        Args:
            z (str): Required. Zoom level.
            x (str): Required. Tile map column. 0 is the leftmost column, at the rightmost column x == 2ᶻ – 1, except for EPSG:4326 projection where x == 2ᶻ⁺¹ – 1.
            y (str): Required. Tile map row. 0 is the top row, for the bottom row y == 2ᶻ – 1.
            map_tile_format (str): Required. Map tile format and resolution. .mvt for a vector tile, @Hx.png for a 256px raster tile (for legacy clients), @1x.png for a 512px raster tile, @2x.png for a 1024px raster tile, @3x.png for a 2048px raster tile, @4x.png for a 4096px raster tile The larger raster tiles are intended for high resolution displays, i.e. 4k monitors and many mobile phones. Available values : .mvt, @Hx.png, @1x.png, @2x.png, @3x.png, @4x.png  
            map_projection (str): Required. Map projection. One of EPSG:3857 (Web Mercator), EPSG:4326 (WGS84 plate careé), EPSG:3575 (Arctic LAEA), EPSG:3031 (Antarctic stereographic) See Projections. Available values : EPSG:3857, EPSG:4326, EPSG:3575, EPSG:3031
            basis_of_record (str): Optional. Basis of record, as defined in our BasisOfRecord vocabulary. Available values : PRESERVED_SPECIMEN, FOSSIL_SPECIMEN, LIVING_SPECIMEN, OBSERVATION, HUMAN_OBSERVATION, MACHINE_OBSERVATION, MATERIAL_SAMPLE, LITERATURE, MATERIAL_CITATION, OCCURRENCE, UNKNOWN
            year (str): Optional. The 4 digit year or year range. A year of 98 will be interpreted as 98 AD..Ranges are written as 1990,2000, 1990, or ,1900.
            verbose (bool): Optional. If set, counts will be grouped by year to allow a fast view of different years. If unset (the default), the total will be a count for all years.
            binning_style (str): Optional. Binning style. hex will aggregate points into a hexagonal grid (see hexPerTile). square will aggregate into a square grid (see squareSize). Available values : hex, square
            hex_per_tile (int): Optional. With bin=hex, sets the number of hexagons horizontally across a tile. Default value : 51
            square_size (str): Optional. With bin=square, sets the size of the squares in pixels on a 4096px tile. Choose a factor of 4096 so they tessalete correctly. Available values : 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096
            map_style (str): Optional. Raster map style — only applies to raster (PNG) tiles. Choose from one of the available styles, the default is classic.point. Styles ending with .point should only be used by non-binned tiles. Styles ending with .poly or .marker. should be used with hexagonal- or square-binned tiles. Available values : purpleHeat.point, blueHeat.point, orangeHeat.point, greenHeat.point, classic.point, purpleYellow.point, green.point, fire.point, glacier.point, classic.poly, classic-noborder.poly, purpleYellow.poly, purpleYellow-noborder.poly, green.poly, green-noborder.poly, green2.poly, iNaturalist.poly, purpleWhite.poly, red.poly, blue.marker, orange.marker, outline.poly, scaled.circles
            country (str): Optional. The 2-letter country code (as per ISO-3166-1) of the country in which the occurrence was recorded. See this endpoint's docs for available values.
            taxon_key (int): Optional. A taxon key from the GBIF backbone.
            dataset_key (str): Optional. The occurrence dataset key (a UUID).
            publishing_org (str): Optional. The publishing organization's GBIF key (a UUID).
            publishing_country (str): Optional. The 2-letter country code (as per ISO-3166-1) of the owning organization's country. See this endpoint's docs for available values.
            network_key (str): Optional. The network's GBIF key (a UUID).
        
        Returns:
            image, str: Saves an image, opens image in browser, or returns URL to image.
        """
        primary_params = {
            'taxonKey': taxon_key,
            'datasetKey': dataset_key,
            'networkKey': network_key,
            'publishingOrg': publishing_org,
            'publishingCountry': publishing_country
        }
        
        # Check how many primary parameters are provided
        primary_params_provided = [key for key, value in primary_params.items() if value is not None]
        
        if len(primary_params_provided) > 1:
            raise ValueError("Only one primary search parameter is permitted: taxonKey, datasetKey, networkKey, publishingOrg, publishingCountry.")
        
        params: Dict[str, Any] = {}
        params_list = [
            ("srs", map_projection),
            ("basisOfRecord", basis_of_record),
            ("year", year),
            ("verbose", verbose),
            ("bin", binning_style),
            ("hexPerTile", hex_per_tile),
            ("squareSize", square_size),
            ("style", map_style),
            ("country", country),
            ("taxonKey", taxon_key),
            ("datasetKey", dataset_key),
            ("publishingOrg", publishing_org),
            ("publishingCountry", publishing_country),
            ("networkKey", network_key)
        ]
        
        hc.add_params(params, params_list)
        resource = f"/adhoc/{z}/{x}/{y}{map_tile_format}"
        
        try:
            response = requests.get(url=base_url+self.endpoint+resource, params=params)
            response.raise_for_status()
        except HTTPError as http_err:
            return hc.handle_error(response, f"HTTP error occurred: {http_err}")
        except Timeout:
            return {"error": "Request timed out."}
        except RequestException as req_err:
            return {"error": f"Request exception occurred: {req_err}"}
        except Exception as err:
            return {"error": f"An unexpected error occurred: {err}"}
        
        image = response.content
        image_url = response.url
        
        # Process image with Pillow
        pil_image = Image.open(BytesIO(image))
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(pil_image)
        pil_image = enhancer.enhance(2.0)  # Increase sharpness

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(pil_image)
        pil_image = enhancer.enhance(1.5)  # Increase contrast

        # Save or display the enhanced image
        if self.save_image and not self.open_in_browser:
            image_file_name = input("Provide a file name for your image: ")
            pil_image.save(image_file_name)
            return "Image saved."
        
        if self.open_in_browser and not self.save_image:
            webbrowser.open(image_url)  # This opens the image in the browser
            return "Opening image in your browser."
        
        if self.open_in_browser and self.save_image:
            image_file_name = input("Provide a file name for your image: ")
            pil_image.save(image_file_name)
            webbrowser.open(image_url)  # This opens the image in the browser
            return "Image saved. Opening image in your browser."
        
        if not self.open_in_browser and not self.save_image:
            return image_url
            
            
    def get_density_tile_map_summary(self,
                                   basis_of_record: Optional[str]=None,
                                   year: Optional[str]=None,
                                   country: Optional[str]=None,
                                   taxon_key: Optional[int]=None,
                                   dataset_key: Optional[str]=None,
                                   publishing_org: Optional[str]=None,
                                   publishing_country: Optional[str]=None,
                                   network_key: Optional[str]=None):
        """
        A summary of the data available for a density tile query. It accepts the same search parameters as the density tile query.  
        
        Args:
            basis_of_record (str): Optional. Basis of record, as defined in our BasisOfRecord vocabulary. Available values : PRESERVED_SPECIMEN, FOSSIL_SPECIMEN, LIVING_SPECIMEN, OBSERVATION, HUMAN_OBSERVATION, MACHINE_OBSERVATION, MATERIAL_SAMPLE, LITERATURE, MATERIAL_CITATION, OCCURRENCE, UNKNOWN
            year (str): Optional. The 4 digit year or year range. A year of 98 will be interpreted as 98 AD..Ranges are written as 1990,2000, 1990, or ,1900.
            country (str): Optional. The 2-letter country code (as per ISO-3166-1) of the country in which the occurrence was recorded. See this endpoint's docs for available values.
            taxon_key (int): Optional. A taxon key from the GBIF backbone.
            dataset_key (str): Optional. The occurrence dataset key (a UUID).
            publishing_org (str): Optional. The publishing organization's GBIF key (a UUID).
            publishing_country (str): Optional. The 2-letter country code (as per ISO-3166-1) of the owning organization's country. See this endpoint's docs for available values.
            network_key (str): Optional. The network's GBIF key (a UUID).
        
        Returns:
            dict: A dictionary containing the summary information.
        """
        primary_params = {
            'taxonKey': taxon_key,
            'datasetKey': dataset_key,
            'networkKey': network_key,
            'publishingOrg': publishing_org,
            'publishingCountry': publishing_country
        }
        
        # Check how many primary parameters are provided
        primary_params_provided = [key for key, value in primary_params.items() if value is not None]
        
        if len(primary_params_provided) > 1:
            raise ValueError("Only one primary search parameter is permitted: taxonKey, datasetKey, networkKey, publishingOrg, publishingCountry.")
        
        params: Dict[str, Any] = {}
        params_list = [
            ("basisOfRecord", basis_of_record),
            ("year", year),
            ("country", country),
            ("taxonKey", taxon_key),
            ("datasetKey", dataset_key),
            ("publishingOrg", publishing_org),
            ("publishingCountry", publishing_country),
            ("networkKey", network_key)
        ]
        
        hc.add_params(params, params_list)
        resource = "/density/capabilities.json"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
        
    def ad_hoc_search_tile(self, z, x, y, map_tile_format, map_projection,
                                   basis_of_record: Optional[str]=None,
                                   year: Optional[str]=None,
                                   binning_style: Optional[str]=None,
                                   hex_per_tile: Optional[int]=None,
                                   square_size: Optional[str]=None,
                                   mode: Optional[str]=None,
                                   map_style: Optional[str]=None,
                                   country: Optional[str]=None,
                                   taxon_key: Optional[int]=None,
                                   dataset_key: Optional[str]=None,
                                   publishing_org: Optional[str]=None,
                                   publishing_country: Optional[str]=None,
                                   network_key: Optional[str]=None):
        """
        Retrieves a tile showing occurrence locations in Mapbox Vector Tile format. Tiles contain a single layer occurrence. Features in that layer are either points (default) or polygons (if chosen). Each feature has a total value; that is the number of occurrences at that point or in the polygon. One primary search parameter is permitted, from these: taxonKey, datasetKey, country, networkKey, publishingOrg, publishingCountry. This can be combined with the parameter country, this limits the primary search to occurrences in that country.
    
        Args:
            z (str): Required. Zoom level.
            x (str): Required. Tile map column. 0 is the leftmost column, at the rightmost column x == 2ᶻ – 1, except for EPSG:4326 projection where x == 2ᶻ⁺¹ – 1.
            y (str): Required. Tile map row. 0 is the top row, for the bottom row y == 2ᶻ – 1.
            map_tile_format (str): Required. Map tile format and resolution. .mvt for a vector tile, @Hx.png for a 256px raster tile (for legacy clients), @1x.png for a 512px raster tile, @2x.png for a 1024px raster tile, @3x.png for a 2048px raster tile, @4x.png for a 4096px raster tile The larger raster tiles are intended for high resolution displays, i.e. 4k monitors and many mobile phones. Available values : .mvt, @Hx.png, @1x.png, @2x.png, @3x.png, @4x.png  
            map_projection (str): Required. Map projection. One of EPSG:3857 (Web Mercator), EPSG:4326 (WGS84 plate careé), EPSG:3575 (Arctic LAEA), EPSG:3031 (Antarctic stereographic) See Projections. Available values : EPSG:3857, EPSG:4326, EPSG:3575, EPSG:3031
            basis_of_record (str): Optional. Basis of record, as defined in our BasisOfRecord vocabulary. Available values : PRESERVED_SPECIMEN, FOSSIL_SPECIMEN, LIVING_SPECIMEN, OBSERVATION, HUMAN_OBSERVATION, MACHINE_OBSERVATION, MATERIAL_SAMPLE, LITERATURE, MATERIAL_CITATION, OCCURRENCE, UNKNOWN
            year (str): Optional. The 4 digit year or year range. A year of 98 will be interpreted as 98 AD..Ranges are written as 1990,2000, 1990, or ,1900.
            binning_style (str): Optional. Binning style. hex will aggregate points into a hexagonal grid (see hexPerTile). square will aggregate into a square grid (see squareSize). Available values : hex, square
            hex_per_tile (int): Optional. With bin=hex, sets the number of hexagons horizontally across a tile. Default value : 51
            square_size (str): Optional. With bin=square, sets the size of the squares in pixels on a 4096px tile. Choose a factor of 4096 so they tessalete correctly. Available values : 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096
            mode (str): Optional. Sets the search mode. GEO_BOUNDS is the default, and returns rectangles that bound all the occurrences in each bin. GEO_CENTROID instead returns a point at the weighted centroid of the bin. Available values : GEO_BOUNDS, GEO_CENTROID
            map_style (str): Optional. Raster map style — only applies to raster (PNG) tiles. Choose from one of the available styles, the default is classic.point. Styles ending with .point should only be used by non-binned tiles. Styles ending with .poly or .marker. should be used with hexagonal- or square-binned tiles. Available values : purpleHeat.point, blueHeat.point, orangeHeat.point, greenHeat.point, classic.point, purpleYellow.point, green.point, fire.point, glacier.point, classic.poly, classic-noborder.poly, purpleYellow.poly, purpleYellow-noborder.poly, green.poly, green-noborder.poly, green2.poly, iNaturalist.poly, purpleWhite.poly, red.poly, blue.marker, orange.marker, outline.poly, scaled.circles
            country (str): Optional. The 2-letter country code (as per ISO-3166-1) of the country in which the occurrence was recorded. See this endpoint's docs for available values.
            taxon_key (int): Optional. A taxon key from the GBIF backbone.
            dataset_key (str): Optional. The occurrence dataset key (a UUID).
            publishing_org (str): Optional. The publishing organization's GBIF key (a UUID).
            publishing_country (str): Optional. The 2-letter country code (as per ISO-3166-1) of the owning organization's country. See this endpoint's docs for available values.
            network_key (str): Optional. The network's GBIF key (a UUID).
        
        Returns:
            image, str: Saves an image, opens image in browser, or returns URL to image.
        """
        primary_params = {
            'taxonKey': taxon_key,
            'datasetKey': dataset_key,
            'networkKey': network_key,
            'publishingOrg': publishing_org,
            'publishingCountry': publishing_country
        }
        
        # Check how many primary parameters are provided
        primary_params_provided = [key for key, value in primary_params.items() if value is not None]
        
        if len(primary_params_provided) > 1:
            raise ValueError("Only one primary search parameter is permitted: taxonKey, datasetKey, networkKey, publishingOrg, publishingCountry.")
        
        params: Dict[str, Any] = {}
        params_list = [
            ("srs", map_projection),
            ("basisOfRecord", basis_of_record),
            ("year", year),
            ("bin", binning_style),
            ("hexPerTile", hex_per_tile),
            ("squareSize", square_size),
            ("mode", mode),
            ("style", map_style),
            ("country", country),
            ("taxonKey", taxon_key),
            ("datasetKey", dataset_key),
            ("publishingOrg", publishing_org),
            ("publishingCountry", publishing_country),
            ("networkKey", network_key)
        ]
        
        hc.add_params(params, params_list)
        resource = f"/density/{z}/{x}/{y}{map_tile_format}"
        
        try:
            response = requests.get(url=base_url+self.endpoint+resource, params=params)
            response.raise_for_status()
        except HTTPError as http_err:
            return hc.handle_error(response, f"HTTP error occurred: {http_err}")
        except Timeout:
            return {"error": "Request timed out."}
        except RequestException as req_err:
            return {"error": f"Request exception occurred: {req_err}"}
        except Exception as err:
            return {"error": f"An unexpected error occurred: {err}"}
        
        image = response.content
        image_url = response.url
        
        # Process image with Pillow
        pil_image = Image.open(BytesIO(image))
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(pil_image)
        pil_image = enhancer.enhance(2.0)  # Increase sharpness

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(pil_image)
        pil_image = enhancer.enhance(1.5)  # Increase contrast

        # Save or display the enhanced image
        if self.save_image and not self.open_in_browser:
            image_file_name = input("Provide a file name for your image: ")
            pil_image.save(image_file_name)
            return "Image saved."
        
        if self.open_in_browser and not self.save_image:
            webbrowser.open(image_url)  # This opens the image in the browser
            return "Opening image in your browser."
        
        if self.open_in_browser and self.save_image:
            image_file_name = input("Provide a file name for your image: ")
            pil_image.save(image_file_name)
            webbrowser.open(image_url)  # This opens the image in the browser
            return "Image saved. Opening image in your browser."
        
        if not self.open_in_browser and not self.save_image:
            return image_url
           
        