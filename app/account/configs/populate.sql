INSERT INTO aggregation_input_class(code, color, description, name_short, name_long) VALUES ('10', '#FFFB6E', null, null, 'Cropland, rainfed'), ('11', '#FFFB6E', null, null, 'Herbaceous cover'), ('12', '#FFFB6E', null, null, 'Tree or shrub cover'), ('20', '#76F1EF', null, null, 'Cropland, irrigated or post-flooding'), ('30', '#DAEC6C', null, null, 'Mosaic cropland (>50%) / natural vegetation (tree, shrub, herbaceous cover) (<50%)'), ('40', '#CDC369', null, null, 'Mosaic natural vegetation (tree, shrub, herbaceous cover) (>50%) / cropland (<50%)'), ('50', '#006313', null, null, 'Tree cover, broadleaved, evergreen, closed to open (>15%)'), ('60', '#009E1D', null, null, 'Tree cover, broadleaved, deciduous, closed to open (>15%)'), ('61', '#009E1D', null, null, 'Tree cover, broadleaved, deciduous, closed (>40%)'), ('62', '#A3C329', null, null, 'Tree cover, broadleaved, deciduous, open (15-40%)'), ('70', '#003E0C', null, null, 'Tree cover, needleleaved, evergreen, closed to open (>15%)'), ('71', '#003E0C', null, null, 'Tree cover, needleleaved, evergreen, closed (>40%)'), ('72', '#00500F', null, null, 'Tree cover, needleleaved, evergreen, open (15-40%)'), ('80', '#00500F', null, null, 'Tree cover, needleleaved, deciduous, closed to open (>15%)'), ('81', '#00500F', null, null, 'Tree cover, needleleaved, deciduous, closed (>40%)'), ('82', '#006313', null, null, 'Tree cover, needleleaved, deciduous, open (15-40%)'), ('90', '#787F1B', null, null, 'Tree cover, mixed leaf type (broadleaved and needleleaved)'), ('100', '#8A9C21', null, null, 'Mosaic tree and shrub (>50%) / herbaceous cover (<50%)'), ('110', '#D09022', null, null, 'Mosaic herbaceous cover (>50%) / tree and shrub (<50%)'), ('120', '#A86019', null, null, 'Shrubland'), ('121', '#874913', null, null, 'Shrubland evergreen'), ('122', '#A86019', null, null, 'Shrubland deciduous'), ('130', '#FFAC42', null, null, 'Grassland'), ('140', '#FFD9D1', null, null, 'Lichens and mosses'), ('150', '#FFE7B0', null, null, 'Sparse vegetation (tree, shrub, herbaceous cover) (<15%)'), ('151', '#FFC16A', null, null, 'Sparse trees (<15%)'), ('152', '#FFCC7C', null, null, 'Sparse shrub (<15%)'), ('153', '#FFE7B0', null, null, 'Sparse herbaceous cover (<15%)'), ('160', '#00785B', null, null, 'Tree cover, flooded, fresh or brakish water'), ('170', '#009577', null, null, 'Tree cover, flooded, saline water'), ('180', '#00DB84', null, null, 'Shrub or herbaceous cover, flooded, fresh/saline/brakish water'), ('190', '#E60017', null, null, 'Urban areas'), ('200', '#FFF3D7', null, null, 'Bare areas'), ('201', '#DCDCDC', null, null, 'Consolidated bare areas'), ('202', '#FFF3D7', null, null, 'Unconsolidated bare areas'), ('210', '#0053C4', null, null, 'Water bodies'), ('220', '#FFFFFF', null, null, 'Permanent snow and ice'), ('-32768', '#000000', null, 'No data', 'No data');

INSERT INTO aggregation_output_class(code, color, description, name_short, name_long) VALUES ('1', '#787F1B', null, 'Tree-covered', 'Tree-covered'), ('2', '#FFAC42', null, 'Grassland', 'Grassland'), ('3', '#FFFB6E', null, 'Cropland', 'Cropland'), ('4', '#00DB84', null, 'Wetland', 'Wetland'), ('5', '#E60017', null, 'Artificial', 'Artificial'), ('6', '#FFF3D7', null, 'Bar land', 'Other land'), ('7', '#0053C4', null, 'Water body', 'Water body'), ('-32768', '#000000', null, 'No data', 'No data');

INSERT INTO script(id, deleted, name, version, description, name_readable, additional_configuration, parametrization_dialogue, run_mode, uid) 
VALUES 
(2, False, 'change-biomass-summary-table', '1.0.9', 'Calculate potential change in biomass with restoration', 'Biomass change (summary)', 'null', null, 'local', null), 
(3, False, 'download-data', '1.99.6', 'Download data from Google Earth Engine assets.', 'Download raw data', 'null', null, 'remote', '471f54dd-0d86-435c-a294-b2c453a02913'), 
(4, False, 'download-landpks', '1.0.9', 'Download LandPKS data', 'Download LandPKS data', 'null', null, 'local', null), 
(5, False, 'drought-vulnerability', '1.99.6', 'Calculate indicators of drought vulnerability', 'Drought vulnerability', 'null', null, 'remote', '441b4cbc-62fe-44ae-a8c0-323cf894530e'), 
(6, False, 'drought-vulnerability-summary', '1.0.9', 'Calculate change in drought vulnerability indicators', 'Drought vulnerability summary', 'null', null, 'local', null), 
(7, False, 'land-cover', '1.0.9', 'Calculate land cover change', 'Land cover change', 'null', null, 'remote', 'e4c5a265-3b25-4f4b-8b30-4f621991fbd1'), 
(8, False, 'local-land-cover', '1.0.9', 'Calculate land cover change', 'Land cover change', 'null', null, 'local', null), 
(9, False, 'local-soil-organic-carbon', '1.99.6', 'Calculate change in soil organic carbon', 'Soil organic carbon change', 'null', null, 'local', null), 
(10, False, 'local-total-carbon', '1.99.6', 'Calculate emissions due to deforestation', 'Total carbon change', 'null', null, 'local', null), 
(11, False, 'productivity', '1.99.6', 'Calculate productivity state, performance, and/or trajectory indicators', 'Land productivity', 
'{
            "trajectory functions": {
                "NDVI trends": {
                    "climate types": [],
                    "description": "Calculate trend of annually integrated NDVI.",
                    "params": {
                        "trajectory_method": "ndvi_trend"
                    }
                },
                "Pixel RESTREND": {
                    "climate types": [
                        "Precipitation",
                        "Soil moisture",
                        "Evapotranspiration"
                    ],
                    "description": "Calculate pixel residual trend (RESTREND of annually integrated NDVI, after removing trend associated with a climate indicator.",
                    "params": {
                        "trajectory_method": "p_restrend"
                    }
                },
                "Rain Use Efficiency (RUE)": {
                    "climate types": [
                        "Precipitation"
                    ],
                    "description": "Calculate rain use efficiency (precipitation divided by NDVI).",
                    "params": {
                        "trajectory_method": "ue"
                    }
                },
                "Water Use Efficiency (WUE)": {
                    "climate types": [
                        "Evapotranspiration"
                    ],
                    "description": "Calculate water use efficiency (evapotranspiration divided by NDVI).",
                    "params": {
                        "trajectory_method": "ue"
                    }
                }
            }
        }' , null, 'remote', '132b2e54-b345-421b-acc3-8fd8f0d09cb7'), 
(12, False, 'restoration-biomass', '1.99.6', 'Calculate potential change in biomass with restoration', 'Biomass change', 'null', null, 'remote', 'a1cce137-e03d-4f42-aa4a-24ac8a503196'), 
(13, False, 'sdg-15-3-1-sub-indicators', '1.99.6', 'Calculate all three SDG 15.3.1 sub-indicators in one step', 'SDG 15.3.1 sub-indicators', 'null', null, 'remote', 'fae0b73f-549d-49a8-b2f6-0769e449332a'), 
(14, False, 'sdg-15-3-1-summary', '1.0.9', 'Calculate change in SDG 15.3.1', 'SDG 15.3.1', 'null', null, 'local', null), 
(15, False, 'soil-organic-carbon', '1.99.6', 'Calculate change in soil organic carbon', 'Soil organic carbon change', 'null', null, 'remote', '2583ebf5-b556-4db3-8d08-d1e14dd39f36'), 
(16, False, 'time-series', '1.99.6', 'Calculates time series of Trends.Earth data', 'Time series', 'null', null, 'remote', '611144f1-17dc-4cb6-a55f-1f998253725e'), 
(17, False, 'total-carbon', '1.99.6', 'Calculates total carbon in biomass (above and below ground).', 'Total carbon change', 'null', null, 'remote', '40b534a7-b82d-4b17-99d8-2b0ab1031fb6'), 
(18, False, 'total-carbon-summary', '1.0.9', null, 'Total carbon change (summary)', 'null', null, 'local', null), 
(19, False, 'unccd-default-data', '1.0.9', 'Generate default data for UNCCD reporting', 'UNCCD default data', 'null', null, 'remote', '68b94101-496e-4f40-a3be-dccc3d701099'), 
(20, False, 'unccd-report', '1.0.9', 'Generate package for UNCCD reporting', 'UNCCD reporting package', 'null', null, 'local', null), 
(21, False, 'urban-area', '1.99.6', 'Calculate change in urban area, in support of SDG 11.3.1', 'Urban area change (summary)', 'null', null, 'remote', 'bb181fc5-b80d-437b-9c94-7374ac0074f4'), 
(22, False, 'urban-change-summary-table', '1.0.9', 'Summarizes urban area change (land consumption rate)', 'Urban area change (summary)', 'null', null, 'local', null);


INSERT INTO algorithm(id, parent_id, deleted, brief_description, description, uid, name, name_details) VALUES 
(2, null, False, null, null, null, 'SDG 15.3.1', 'Land degradation'), 
(3, null, False, null, null, null, 'Drought', 'Vulnerability and exposure'), 
(4, null, False, null, null, null, 'UNCCD Reporting', 'Summarize data for reporting'), 
(5, null, False, null, null, null, 'SDG 11.3.1', 'Urban change and land consumption'),
(6, null, False, null, null, null, 'Experimental', null), 
(7, 2, False, null, 'Calculate SDG 15.3.1 sub-indicators (required prior to 15.3.1 indicator calculation)', 'bdad3786-bc36-46aa-8e3d-d6cede915cef', 'Sub-indicators for SDG 15.3.1', null),
(8, 2, False, null, 'Calculate SDG 15.3.1 indicator from productivity, land cover, and soil organic carbon sub-indicators', 'fe1cffa7-33f7-4148-ac7b-fc726402d59d', 'Indicator for SDG 15.3.1', 'Spatial layer and summary table for total boundary'), 
(9, 2, False, null, 'Land productivity is the biological productive capacity of land', 'e25d2a72-2274-45fa-9b69-74e87873054e', 'Land productivity', null), 
(10, 2, False, null, 'Land cover is the physical material at the surface of the earth. ', '277f87e6-5362-4533-ab1d-c28251576884', 'Land cover change', null), 
(11, 2, False, null, 'Soil organic carbon is a measure of soil organic matter', 'f32fd29b-2af8-4564-9189-3dd440758be6', 'Soil Organic Carbon', null), 
(12, 3, False, null, 'Calculate indicators of drought vulnerability consistent with UNCCD SO3 Good Practice Guidance', 'afb8d95a-20a5-11ec-9621-0242ac130002', 'Drought vulnerability', null), 
(13, 3, False, null, 'Summarize drought indicators in alignment with UNCCD SO3 reporting requirements', 'bb5df452-20a5-11ec-9621-0242ac130002', 'Drought vulnerability summary table', null), 
(14, 4, False, null, 'Generate default datasets used in the UNCCD 2021 reporting cycle', '052b3fbc-20a7-11ec-9621-0242ac130002', 'Default data for UNCCD reporting', null), 
(15, 4, False, null, 'Summarize Strategic Objective (SO) 1, SO2, and SO3 datasets in proper format for submission to UNCCD for 2021 reporting cycle', '5293b2b2-d90f-4f1f-9556-4b0fe1c6ba91', 'Generate data package for UNCCD reporting', null), 
(16, 5, False, null, 'Calculate indicators of change in urban extent (SDG 11.3.1 indicator)', 'bdce0a12-c5ab-485b-ac47-278cedbce789', 'Urban change spatial layer', null), 
(17, 5, False, null, 'Calculate table summarizing SDG indicator 11.3.1', '748780b4-39bb-4460-b203-0f2367d7c699', 'Urban change summary table for city', null), 
(18, 6, False, null, null, null, 'Calculate change in total carbon', 'Above and below ground, emissions and deforestation'), 
(19, 6, False, null, null, null, 'Potential change in biomass due to restoration', 'Above and below ground woody'), 
(20, 18, False, null, 'Calculate total carbon (above and below-ground) and emissions from deforestation', '96f243a2-c8bd-436a-9775-424f20a1b188', 'Calculate change in carbon', null), 
(21, 18, False, null, 'Calculate table summarizing change in total carbon', 'a753f2c9-be4c-4d97-9e21-09b8882e8899', 'Change in carbon summary table', null), 
(22, 19, False, null, 'Estimate potential change in biomass due to restoration', '61839d52-0d81-428d-90e6-83ea5ed3c032', 'Estimate potential impacts of restoration', null), 
(23, 19, False, null, 'Generate table summarizing potential change in biomass due to restoration', 'cb425356-09cf-4390-89dc-8542cdf0805c', 'Table summarizing likely changes in biomass', null);

INSERT INTO algorithm_script(id, algorithm_id, script_id) VALUES 
(23, 22, 12), 
(24, 23, 2), 
(25, 20, 10), 
(26, 20, 17), 
(27, 21, 18), 
(28, 7, 13), 
(29, 8, 14), 
(30, 9, 11), 
(31, 10, 8), 
(32, 10, 7), 
(33, 11, 9), 
(34, 11, 15), 
(35, 12, 5), 
(36, 13, 6), 
(37, 14, 19), 
(38, 15, 20), 
(39, 16, 21), 
(40, 17, 22);

INSERT INTO continent(geom, code, name) VALUES (null, null, 'Asia'), (null, null, 'South America'), (null, null, 'North America'), (null, null, 'Oceania'), (null, null, 'Antarctica'), (null, null, 'Africa'), (null, null, 'Seven seas (open ocean)'), (null, null, 'Europe');

INSERT INTO job_status(code, value) VALUES ('READY', 'READY'), ('PENDING', 'PENDING'), ('FINISHED', 'FINISHED'), ('RUNNING', 'RUNNING'), ('FAILED', 'FAILED'), ('DELETED', 'DELETED'), ('DOWNLOADED', 'DOWNLOADED'), ('GENERATED_LOCALLY', 'GENERATED_LOCALLY'), ('CANCELLED', 'CANCELLED');

INSERT INTO user_aggregation_class(inputclass_id, outputclass_id, user_id) 
VALUES 
    (38, 8, null), 
    (7, 1, null), 
    (8, 1, null), 
    (9, 1, null), 
    (10, 1, null), 
    (11, 1, null), 
    (12, 1, null), 
    (13, 1, null), 
    (14, 1, null), 
    (15, 1, null), 
    (16, 1, null), 
    (17, 1, null), 
    (18, 1, null), 
    (19, 2, null), 
    (20, 2, null), 
    (21, 2, null), 
    (22, 2, null), 
    (23, 2, null), 
    (24, 2, null), 
    (25, 2, null), 
    (26, 2, null), 
    (27, 2, null), 
    (28, 2, null), (1, 3, null), (2, 3, null), (3, 3, null), (4, 3, null), (5, 3, null), (6, 3, null), (29, 4, null), (30, 4, null), (31, 4, null), (32, 5, null), (33, 6, null), (34, 6, null), (35, 6, null), (37, 6, null), (36, 7, null);

INSERT INTO account_roles(code, value) 
    VALUES 
        ('ADMIN', 'Admin'),
        ('USER', 'User');


INSERT INTO lc_matrix(id, user_id, name, content) 
    VALUES 
    (1, null, 'Default', '{
    "name": "UNCCD default land cover degradation transition matrix",
    "legend": {
        "key": [
            {
                "code": 1,
                "color": "#787F1B",
                "description": null,
                "name_long": "Tree-covered",
                "name_short": "Tree-covered"
            },
            {
                "code": 2,
                "color": "#FFAC42",
                "description": null,
                "name_long": "Grassland",
                "name_short": "Grassland"
            },
            {
                "code": 3,
                "color": "#FFFB6E",
                "description": null,
                "name_long": "Cropland",
                "name_short": "Cropland"
            },
            {
                "code": 4,
                "color": "#00DB84",
                "description": null,
                "name_long": "Wetland",
                "name_short": "Wetland"
            },
            {
                "code": 5,
                "color": "#E60017",
                "description": null,
                "name_long": "Artificial",
                "name_short": "Artificial"
            },
            {
                "code": 6,
                "color": "#FFF3D7",
                "description": null,
                "name_long": "Other land",
                "name_short": "Other land"
            },
            {
                "code": 7,
                "color": "#0053C4",
                "description": null,
                "name_long": "Water body",
                "name_short": "Water body"
            }
        ],
        "name": "UNCCD Land Cover",
        "nodata": {
            "code": -32768,
            "name_long": "No data",
            "name_short": "No data",
            "description": null,
            "color": "#000000"
        }
    },
    "definitions": {
        "name": "Land cover degradation transition meanings",
        "transitions": [
            {
                "final": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "initial": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "initial": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "meaning": "improvement"
            },
            {
                "final": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "initial": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "initial": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "initial": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "initial": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "initial": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "initial": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "initial": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "initial": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "initial": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "initial": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "initial": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "initial": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "initial": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "meaning": "improvement"
            },
            {
                "final": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "initial": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "meaning": "improvement"
            },
            {
                "final": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "initial": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "initial": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "initial": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "initial": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "initial": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "initial": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "initial": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "initial": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "initial": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "initial": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "initial": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "initial": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "initial": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "meaning": "improvement"
            },
            {
                "final": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "initial": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "meaning": "improvement"
            },
            {
                "final": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "initial": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "meaning": "improvement"
            },
            {
                "final": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "initial": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "meaning": "improvement"
            },
            {
                "final": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "initial": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "initial": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "meaning": "improvement"
            },
            {
                "final": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "initial": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "initial": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "meaning": "improvement"
            },
            {
                "final": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "initial": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "meaning": "improvement"
            },
            {
                "final": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "initial": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "meaning": "improvement"
            },
            {
                "final": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "initial": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "meaning": "improvement"
            },
            {
                "final": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "initial": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "meaning": "degradation"
            },
            {
                "final": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "initial": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "initial": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 3,
                    "color": "#FFFB6E",
                    "description": null,
                    "name_long": "Cropland",
                    "name_short": "Cropland"
                },
                "initial": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 1,
                    "color": "#787F1B",
                    "description": null,
                    "name_long": "Tree-covered",
                    "name_short": "Tree-covered"
                },
                "initial": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 2,
                    "color": "#FFAC42",
                    "description": null,
                    "name_long": "Grassland",
                    "name_short": "Grassland"
                },
                "initial": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 4,
                    "color": "#00DB84",
                    "description": null,
                    "name_long": "Wetland",
                    "name_short": "Wetland"
                },
                "initial": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 5,
                    "color": "#E60017",
                    "description": null,
                    "name_long": "Artificial",
                    "name_short": "Artificial"
                },
                "initial": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 6,
                    "color": "#FFF3D7",
                    "description": null,
                    "name_long": "Other land",
                    "name_short": "Other land"
                },
                "initial": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "meaning": "stable"
            },
            {
                "final": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "initial": {
                    "code": 7,
                    "color": "#0053C4",
                    "description": null,
                    "name_long": "Water body",
                    "name_short": "Water body"
                },
                "meaning": "stable"
            }
        ]
    }
}');


SELECT setval('algorithm_id_seq', (SELECT MAX(id) FROM algorithm));
SELECT setval('execution_script_id_seq', (SELECT MAX(id) FROM script));
SELECT setval('algorithm_scripts_id_seq', (SELECT MAX(id) FROM algorithm_script));
SELECT setval('lc_matrix_id_seq', (SELECT MAX(id) FROM lc_matrix));