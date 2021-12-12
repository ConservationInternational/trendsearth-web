INSERT INTO aggregation_input_class(code, color, description, name_short, name_long) VALUES ('10', '#FFFB6E', null, null, 'Cropland, rainfed'), ('11', '#FFFB6E', null, null, 'Herbaceous cover'), ('12', '#FFFB6E', null, null, 'Tree or shrub cover'), ('20', '#76F1EF', null, null, 'Cropland, irrigated or post-flooding'), ('30', '#DAEC6C', null, null, 'Mosaic cropland (>50%) / natural vegetation (tree, shrub, herbaceous cover) (<50%)'), ('40', '#CDC369', null, null, 'Mosaic natural vegetation (tree, shrub, herbaceous cover) (>50%) / cropland (<50%)'), ('50', '#006313', null, null, 'Tree cover, broadleaved, evergreen, closed to open (>15%)'), ('60', '#009E1D', null, null, 'Tree cover, broadleaved, deciduous, closed to open (>15%)'), ('61', '#009E1D', null, null, 'Tree cover, broadleaved, deciduous, closed (>40%)'), ('62', '#A3C329', null, null, 'Tree cover, broadleaved, deciduous, open (15-40%)'), ('70', '#003E0C', null, null, 'Tree cover, needleleaved, evergreen, closed to open (>15%)'), ('71', '#003E0C', null, null, 'Tree cover, needleleaved, evergreen, closed (>40%)'), ('72', '#00500F', null, null, 'Tree cover, needleleaved, evergreen, open (15-40%)'), ('80', '#00500F', null, null, 'Tree cover, needleleaved, deciduous, closed to open (>15%)'), ('81', '#00500F', null, null, 'Tree cover, needleleaved, deciduous, closed (>40%)'), ('82', '#006313', null, null, 'Tree cover, needleleaved, deciduous, open (15-40%)'), ('90', '#787F1B', null, null, 'Tree cover, mixed leaf type (broadleaved and needleleaved)'), ('100', '#8A9C21', null, null, 'Mosaic tree and shrub (>50%) / herbaceous cover (<50%)'), ('110', '#D09022', null, null, 'Mosaic herbaceous cover (>50%) / tree and shrub (<50%)'), ('120', '#A86019', null, null, 'Shrubland'), ('121', '#874913', null, null, 'Shrubland evergreen'), ('122', '#A86019', null, null, 'Shrubland deciduous'), ('130', '#FFAC42', null, null, 'Grassland'), ('140', '#FFD9D1', null, null, 'Lichens and mosses'), ('150', '#FFE7B0', null, null, 'Sparse vegetation (tree, shrub, herbaceous cover) (<15%)'), ('151', '#FFC16A', null, null, 'Sparse trees (<15%)'), ('152', '#FFCC7C', null, null, 'Sparse shrub (<15%)'), ('153', '#FFE7B0', null, null, 'Sparse herbaceous cover (<15%)'), ('160', '#00785B', null, null, 'Tree cover, flooded, fresh or brakish water'), ('170', '#009577', null, null, 'Tree cover, flooded, saline water'), ('180', '#00DB84', null, null, 'Shrub or herbaceous cover, flooded, fresh/saline/brakish water'), ('190', '#E60017', null, null, 'Urban areas'), ('200', '#FFF3D7', null, null, 'Bare areas'), ('201', '#DCDCDC', null, null, 'Consolidated bare areas'), ('202', '#FFF3D7', null, null, 'Unconsolidated bare areas'), ('210', '#0053C4', null, null, 'Water bodies'), ('220', '#FFFFFF', null, null, 'Permanent snow and ice'), ('-32768', '#000000', null, 'No data', 'No data');

INSERT INTO aggregation_output_class(code, color, description, name_short, name_long) VALUES ('1', '#787F1B', null, 'Tree-covered', 'Tree-covered'), ('2', '#FFAC42', null, 'Grassland', 'Grassland'), ('3', '#FFFB6E', null, 'Cropland', 'Cropland'), ('4', '#00DB84', null, 'Wetland', 'Wetland'), ('5', '#E60017', null, 'Artificial', 'Artificial'), ('6', '#FFF3D7', null, 'Bar land', 'Other land'), ('7', '#0053C4', null, 'Water body', 'Water body'), ('-32768', '#000000', null, 'No data', 'No data');

INSERT INTO algorithm_runmode(code, value) VALUES ('0', 'NOT_APPLICABLE'), ('local', 'LOCAL'), ('remote', 'REMOTE'), ('both', 'BOTH');

INSERT INTO algorigthm_nodetype(code, value) VALUES ('1', 'Group'), ('2', 'Algorithm'), ('3', 'Details');

INSERT INTO algorithm(item_type_id, parent_id, deleted, description, uid, name, name_details, brief_description) 
    VALUES 
    (1, null, False, null, null, 'SDG 15.3.1', 'Land degradation', null), 
    (1, null, False, null, null, 'Drought', 'Calculate indicators of drought vulnerability and exposure', null), 
    (1, null, False, null, null, 'UNCCD Reporting', 'Summarize data for reporting', null), 
    (1, null, False, null, null, 'SDG 11.3.1', 'Urban Change and Land Consumption', null), 
    (1, null, False, null, null, 'Experimental', null, null), 
    (2, 1, False, 'Calculate Productivity, Land Cover and Soil Organic carbon sub-indicators simultaneously', 'bdad3786-bc36-46aa-8e3d-d6cede915cef', 'All SDG 15.3.1 sub-indicators in one step', null, null), 
    (2, 1, False, 'Proportion of land that is degraded over total land area', 'fe1cffa7-33f7-4148-ac7b-fc726402d59d', 'Main SDG 15.3.1 indicator', 'Spatial layer and summary table for total boundary', null), 
    (2, 1, False, 'Land productivity is the biological productive capacity of the land, the source of all the food, fiber and fuel that sustains humans', 'e25d2a72-2274-45fa-9b69-74e87873054e', 'Land Productivity', null, null), 
    (2, 1, False, 'Land cover is the physical material at the surface of the earth. Land covers include grass, asphalt, trees, bare ground, water, etc', '277f87e6-5362-4533-ab1d-c28251576884', 'Land Cover', null, null), 
    (2, 1, False, 'Soil organic carbon is a measureable component of soil organic matter', 'f32fd29b-2af8-4564-9189-3dd440758be6', 'Soil Organic Carbon', null, null), 
    (2, 2, False, 'Calculate indicators of drought vulnerability consistent with United Nations Convention to Combat Desertification (UNCCD) Good Practice Guidance for Strategic Objective 3 (SO3)', 'afb8d95a-20a5-11ec-9621-0242ac130002', 'Drought vulnerability indicators', null, null),
    (2, 2, False, 'Summarize drought indicators (in alignment with UNCCD SO3 reporting requirements)', 'bb5df452-20a5-11ec-9621-0242ac130002', 'Drought vulnerability summary table', null, null), 
    (2, 3, False, 'Generate the default datasets for submission to United Nations Convention to Combat Desertification (UNCCD), consistent with relevant Good Practice Guidances', '052b3fbc-20a7-11ec-9621-0242ac130002', 'Calculate default data for UNCCD reporting', null, null), 
    (2, 3, False, 'Summarize land degradation, population affected by degradation, and drought datasets for submission to UNCCD', '5293b2b2-d90f-4f1f-9556-4b0fe1c6ba91', 'Generate data package for UNCCD reporting', null, null), 
    (2, 4, False, 'TODO: Urban change spatial layer long description', 'bdce0a12-c5ab-485b-ac47-278cedbce789', 'Urban change spatial layer', null, null), 
    (2, 4, False, 'TODO: Urban change summary table for city long description', '748780b4-39bb-4460-b203-0f2367d7c699', 'Urban change summary table for city', null, null), 
    (2, 5, False, null, null, 'Total carbon', 'Above and below ground, emissions and deforestation', null), 
    (2, 5, False, null, null, 'Potential change in biomass due to restoration', 'Above and below ground woody', null), 
    (2, 17, False, 'TODO: Carbon change spatial layers long description', '96f243a2-c8bd-436a-9775-424f20a1b188', 'Carbon change spatial layers', null, null), 
    (2, 17, False, 'TODO: Carbon change summary table for boundary long description', 'a753f2c9-be4c-4d97-9e21-09b8882e8899', 'Carbon change summary table for boundary', null, null), 
    (2, 18, False, 'TODO: Estimate biomass change long description', '61839d52-0d81-428d-90e6-83ea5ed3c032', 'Estimate biomass change', null, null), 
    (2, 18, False, 'TODO: Table summarizing likely changes in biomass long description', 'cb425356-09cf-4390-89dc-8542cdf0805c', 'Table summarizing likely changes in biomass', null, null);

INSERT INTO script(execution_script_id, parametrization_dialogue) VALUES 
    (12, 'LDMP.calculate_ldn.DlgCalculateOneStep'), 
    (13, 'LDMP.calculate_ldn.DlgCalculateLDNSummaryTableAdmin'), 
    (10, 'LDMP.calculate_prod.DlgCalculateProd'), 
    (7, 'LDMP.calculate_lc.DlgCalculateLC'), 
    (6, 'LDMP.calculate_lc.DlgCalculateLC'), 
    (8, 'LDMP.calculate_soc.DlgCalculateSOC'), 
    (13, 'LDMP.calculate_soc.DlgCalculateSOC'), 
    (4, 'LDMP.calculate_drought_vulnerability.DlgCalculateDrought'), 
    (5, 'LDMP.calculate_drought_vulnerability.DlgCalculateDroughtSummary'), 
    (18, 'LDMP.calculate_unccd.DlgCalculateUNCCD'), 
    (19, 'LDMP.calculate_unccd.DlgCalculateUNCCDReport'), 
    (20, 'LDMP.calculate_urban.DlgCalculateUrbanData'), 
    (21, 'LDMP.calculate_urban.DlgCalculateUrbanSummaryTable'), 
    (16, 'LDMP.calculate_tc.DlgCalculateTCData'), 
    (17, 'LDMP.calculate_tc.DlgCalculateTCSummaryTable'), 
    (11, 'LDMP.calculate_rest_biomass.DlgCalculateRestBiomassData'), 
    (1, 'LDMP.calculate_rest_biomass.DlgCalculateRestBiomassSummaryTable');

INSERT INTO execution_script(run_mode_id, deleted, version, description, name_readable, additional_configuration, uid, name) 
VALUES 
    (2, False, null, 'Calculate potential change in biomass with restoration', 'Biomass change (summary)', 'null', null, 'change-biomass-summary-table'), 
    (3, False, '1.0.9', 'Download data from Google Earth Engine assets.', 'Download raw data', 'null', '6b6c2d67-dbc6-4ee4-a147-16ee5145fb45', 'download-data'), 
    (2, False, null, 'Download LandPKS data', 'Download LandPKS data', 'null', null, 'download-landpks'), 
    (3, False, '1.0.9', 'Calculate indicators of drought vulnerability', 'Drought vulnerability', 'null', '1eb43e75-cbe2-4fd4-80f1-0eca78193275', 'drought-vulnerability'), 
    (2, False, null, 'Calculate change in drought vulnerability indicators', 'Drought vulnerability summary', 'null', null, 'drought-vulnerability-summary'), 
    (3, False, '1.0.9', 'Calculate land cover change', 'Land cover change', 'null', '368306cc-f9f9-4ee1-a83f-1ab9d223ffec', 'land-cover'), 
    (2, False, null, 'Calculate land cover change', 'Land cover change', 'null', null, 'local-land-cover'), 
    (2, False, null, 'Calculate change in soil organic carbon', 'Soil organic carbon change', 'null', null, 'local-soil-organic-carbon'), 
    (2, False, null, 'Calculate emissions due to deforestation', 'Total carbon change', 'null', null, 'local-total-carbon'), 
    (3, False, '1.0.9', 'Calculate productivity state, performance, and/or trajectory indicators', 'Land productivity', 
        '{"NDVI trends": {"climate types": , "description": "Calculate trend of annually integrated NDVI.", "params": {"trajectory_method": "ndvi_trend"}}, "Pixel RESTREND": {"climate types": "Precipitation", "Soil moisture", "Evapotranspiration", "description": "Calculate pixel residual trend (RESTREND of annually integrated NDVI, after removing trend associated with a climate indicator.", "params": {"trajectory_method": "p_restrend"}}, "Rain Use Efficiency (RUE)": {"climate types": "Precipitation", "description": "Calculate rain use efficiency (precipitation divided by NDVI).", "params": {"trajectory_method": "ue"}}, "Water Use Efficiency (WUE)": {"climate types": "Evapotranspiration", "description": "Calculate water use efficiency (evapotranspiration divided by NDVI).", "params": {"trajectory_method": "ue"}}}', '33e52ba6-2666-4227-a537-75907fe0a8a3', 'productivity'), 
    (3, False, '1.0.9', 'Calculate potential change in biomass with restoration', 'Biomass change', 'null', 'ab184b9b-59c5-44af-b3ca-776210f7812b', 'restoration-biomass'), 
    (3, False, '1.11', 'Calculate all three SDG 15.3.1 sub-indicators in one step', 'SDG 15.3.1 sub-indicators', 'null', '48428c55-f803-44a3-83ca-a20cb6947f3c', 'sdg-15-3-1-sub-indicators'), 
    (2, False, null, 'Calculate change in SDG 15.3.1', 'SDG 15.3.1', 'null', null, 'sdg-15-3-1-summary'), 
    (3, False, '1.0.9', 'Calculate change in soil organic carbon', 'Soil organic carbon change', 'null', 'da0c658b-57df-4cef-95b7-51f230d098d6', 'soil-organic-carbon'),
    (3, False, '1.0.9', 'Calculates time series of Trends.Earth data', 'Time series', 'null', '708d9f90-0494-4877-8c08-9045cc72d425', 'time-series'), 
    (3, False, '1.0.9', 'Calculates total carbon in biomass (above and below ground).', 'Total carbon change', 'null', '68b94101-496e-4f40-a3be-dccc3d701099', 'total-carbon'), 
    (2, False, null, null, 'Total carbon change (summary)', 'null', null, 'total-carbon-summary'), 
    (3, False, '1.0.9', 'Generate default data for UNCCD reporting', 'UNCCD default data', 'null', '68b94101-496e-4f40-a3be-dccc3d701099', 'unccd-default-data'), 
    (2, False, null, 'Generate package for UNCCD reporting', 'UNCCD reporting package', 'null', null, 'unccd-report'), 
    (3, False, '1.0.9', 'Calculate change in urban area, in support of SDG 11.3.1', 'Urban area change (summary)', 'null', 'df85ce6c-017e-4ec7-8d46-c0c89f05bb72', 'urban-area'), 
    (2, False, null, 'Summarizes urban area change (land consumption rate)', 'Urban area change (summary)', 'null', null, 'urban-change-summary-table');

INSERT INTO algorithm_scripts(algorithm_id, script_id) 
    VALUES 
        (6, 1), 
        (7, 2), 
        (8, 3), 
        (9, 4), 
        (9, 5), 
        (10, 6), 
        (10, 7), 
        (11, 8), 
        (12, 9), 
        (13, 10), 
        (14, 11), 
        (15, 12), 
        (16, 13), 
        (19, 14), 
        (20, 15), 
        (21, 16), 
        (22, 17);

INSERT INTO continent(geom, code, name) VALUES (null, null, 'Asia'), (null, null, 'South America'), (null, null, 'North America'), (null, null, 'Oceania'), (null, null, 'Antarctica'), (null, null, 'Africa'), (null, null, 'Seven seas (open ocean)'), (null, null, 'Europe');

INSERT INTO job_status(code, value) VALUES ('READY', 'READY'), ('PENDING', 'PENDING'), ('FINISHED', 'FINISHED'), ('RUNNING', 'RUNNING'), ('FAILED', 'FAILED'), ('DELETED', 'DELETED'), ('DOWNLOADED', 'DOWNLOADED'), ('GENERATED_LOCALLY', 'GENERATED_LOCALLY'), ('CANCELLED', 'CANCELLED');

INSERT INTO script_status(code, value) VALUES ('SUCCESS', 'SUCCESS'), ('FAIL', 'FAIL');

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