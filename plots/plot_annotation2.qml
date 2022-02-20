<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" simplifyDrawingTol="1" version="3.22.2-Białowieża" simplifyAlgorithm="0" minScale="100000000" simplifyLocal="1" symbologyReferenceScale="-1" styleCategories="AllStyleCategories" simplifyMaxScale="1" readOnly="1" hasScaleBasedVisibilityFlag="0" simplifyDrawingHints="1" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal durationUnit="min" endExpression="" mode="0" endField="" durationField="" accumulate="0" enabled="0" startField="" startExpression="" limitMode="0" fixedDuration="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 forceraster="0" type="singleSymbol" referencescale="-1" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol name="0" type="fill" force_rhr="0" clip_to_extent="1" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" name="name" type="QString"/>
            <Option name="properties"/>
            <Option value="collection" name="type" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" pass="0" class="SimpleFill">
          <Option type="Map">
            <Option value="3x:0,0,0,0,0,0" name="border_width_map_unit_scale" type="QString"/>
            <Option value="255,255,192,255" name="color" type="QString"/>
            <Option value="bevel" name="joinstyle" type="QString"/>
            <Option value="0,0" name="offset" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
            <Option value="MM" name="offset_unit" type="QString"/>
            <Option value="0,0,0,255" name="outline_color" type="QString"/>
            <Option value="solid" name="outline_style" type="QString"/>
            <Option value="0.26" name="outline_width" type="QString"/>
            <Option value="MM" name="outline_width_unit" type="QString"/>
            <Option value="solid" name="style" type="QString"/>
          </Option>
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="255,255,192,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" locked="0" pass="0" class="GeometryGenerator">
          <Option type="Map">
            <Option value="Marker" name="SymbolType" type="QString"/>
            <Option value="nodes_to_points($geometry)" name="geometryModifier" type="QString"/>
            <Option value="MapUnit" name="units" type="QString"/>
          </Option>
          <prop v="Marker" k="SymbolType"/>
          <prop v="nodes_to_points($geometry)" k="geometryModifier"/>
          <prop v="MapUnit" k="units"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@1" type="marker" force_rhr="0" clip_to_extent="1" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer enabled="1" locked="0" pass="0" class="GeometryGenerator">
              <Option type="Map">
                <Option value="Line" name="SymbolType" type="QString"/>
                <Option value="make_line( point_n( $geometry,(@geometry_part_num)),point_n( $geometry,(@geometry_part_num+1)))" name="geometryModifier" type="QString"/>
                <Option value="MapUnit" name="units" type="QString"/>
              </Option>
              <prop v="Line" k="SymbolType"/>
              <prop v="make_line( point_n( $geometry,(@geometry_part_num)),point_n( $geometry,(@geometry_part_num+1)))" k="geometryModifier"/>
              <prop v="MapUnit" k="units"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties"/>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
              <symbol name="@@0@1@0" type="line" force_rhr="0" clip_to_extent="1" alpha="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option value="" name="name" type="QString"/>
                    <Option name="properties"/>
                    <Option value="collection" name="type" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" locked="0" pass="0" class="MarkerLine">
                  <Option type="Map">
                    <Option value="4" name="average_angle_length" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="average_angle_map_unit_scale" type="QString"/>
                    <Option value="MM" name="average_angle_unit" type="QString"/>
                    <Option value="3" name="interval" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="interval_map_unit_scale" type="QString"/>
                    <Option value="MM" name="interval_unit" type="QString"/>
                    <Option value="2" name="offset" type="QString"/>
                    <Option value="0" name="offset_along_line" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="offset_along_line_map_unit_scale" type="QString"/>
                    <Option value="MM" name="offset_along_line_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
                    <Option value="MM" name="offset_unit" type="QString"/>
                    <Option value="centralpoint" name="placement" type="QString"/>
                    <Option value="0" name="ring_filter" type="QString"/>
                    <Option value="1" name="rotate" type="QString"/>
                  </Option>
                  <prop v="4" k="average_angle_length"/>
                  <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
                  <prop v="MM" k="average_angle_unit"/>
                  <prop v="3" k="interval"/>
                  <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
                  <prop v="MM" k="interval_unit"/>
                  <prop v="2" k="offset"/>
                  <prop v="0" k="offset_along_line"/>
                  <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
                  <prop v="MM" k="offset_along_line_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
                  <prop v="MM" k="offset_unit"/>
                  <prop v="centralpoint" k="placement"/>
                  <prop v="0" k="ring_filter"/>
                  <prop v="1" k="rotate"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option value="" name="name" type="QString"/>
                      <Option name="properties"/>
                      <Option value="collection" name="type" type="QString"/>
                    </Option>
                  </data_defined_properties>
                  <symbol name="@@@0@1@0@0" type="marker" force_rhr="0" clip_to_extent="1" alpha="1">
                    <data_defined_properties>
                      <Option type="Map">
                        <Option value="" name="name" type="QString"/>
                        <Option name="properties"/>
                        <Option value="collection" name="type" type="QString"/>
                      </Option>
                    </data_defined_properties>
                    <layer enabled="1" locked="0" pass="0" class="FontMarker">
                      <Option type="Map">
                        <Option value="0" name="angle" type="QString"/>
                        <Option value="A" name="chr" type="QString"/>
                        <Option value="0,0,0,255" name="color" type="QString"/>
                        <Option value="Arial" name="font" type="QString"/>
                        <Option value="" name="font_style" type="QString"/>
                        <Option value="1" name="horizontal_anchor_point" type="QString"/>
                        <Option value="miter" name="joinstyle" type="QString"/>
                        <Option value="0,0" name="offset" type="QString"/>
                        <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
                        <Option value="MM" name="offset_unit" type="QString"/>
                        <Option value="0,0,0,255" name="outline_color" type="QString"/>
                        <Option value="0" name="outline_width" type="QString"/>
                        <Option value="3x:0,0,0,0,0,0" name="outline_width_map_unit_scale" type="QString"/>
                        <Option value="MM" name="outline_width_unit" type="QString"/>
                        <Option value="1.8" name="size" type="QString"/>
                        <Option value="3x:0,0,0,0,0,0" name="size_map_unit_scale" type="QString"/>
                        <Option value="MM" name="size_unit" type="QString"/>
                        <Option value="1" name="vertical_anchor_point" type="QString"/>
                      </Option>
                      <prop v="0" k="angle"/>
                      <prop v="A" k="chr"/>
                      <prop v="0,0,0,255" k="color"/>
                      <prop v="Arial" k="font"/>
                      <prop v="" k="font_style"/>
                      <prop v="1" k="horizontal_anchor_point"/>
                      <prop v="miter" k="joinstyle"/>
                      <prop v="0,0" k="offset"/>
                      <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
                      <prop v="MM" k="offset_unit"/>
                      <prop v="0,0,0,255" k="outline_color"/>
                      <prop v="0" k="outline_width"/>
                      <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
                      <prop v="MM" k="outline_width_unit"/>
                      <prop v="1.8" k="size"/>
                      <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
                      <prop v="MM" k="size_unit"/>
                      <prop v="1" k="vertical_anchor_point"/>
                      <data_defined_properties>
                        <Option type="Map">
                          <Option value="" name="name" type="QString"/>
                          <Option name="properties" type="Map">
                            <Option name="angle" type="Map">
                              <Option value="true" name="active" type="bool"/>
                              <Option value="CASE WHEN degrees(&#xd;&#xa;&#x9;azimuth(point_n(transform($geometry,@flts_source_crs, 'EPSG:4326') , @geometry_part_num), &#xd;&#xa;&#x9;point_n(transform($geometry,@flts_source_crs, 'EPSG:4326'), @geometry_part_num+1))&#xd;&#xa;&#x9;) > 180 AND degrees(&#xd;&#xa;&#x9;azimuth(point_n(transform($geometry,@flts_source_crs, 'EPSG:4326'), @geometry_part_num), &#xd;&#xa;&#x9;point_n(transform($geometry,@flts_source_crs, 'EPSG:4326'), @geometry_part_num+1))&#xd;&#xa;&#x9;) &lt; 360&#xd;&#xa;&#x9;THEN line_interpolate_angle( transform($geometry,@flts_source_crs, 'EPSG:4326'), 0) + 90&#xd;&#xa;ELSE&#xd;&#xa;&#x9;line_interpolate_angle( transform($geometry,@flts_source_crs, 'EPSG:4326'), 0) + 270&#xd;&#xa;END" name="expression" type="QString"/>
                              <Option value="3" name="type" type="int"/>
                            </Option>
                            <Option name="char" type="Map">
                              <Option value="true" name="active" type="bool"/>
                              <Option value="format_number(&#xd;&#xa;&#x9;length(make_line(&#xd;&#xa;&#x9;point_n($geometry,(@geometry_part_num)),&#xd;&#xa;&#x9;point_n( $geometry,(@geometry_part_num+1))&#xd;&#xa;&#x9;)),&#xd;&#xa;&#x9;2&#xd;&#xa;) ||' m'" name="expression" type="QString"/>
                              <Option value="3" name="type" type="int"/>
                            </Option>
                            <Option name="offset" type="Map">
                              <Option value="false" name="active" type="bool"/>
                              <Option value="" name="field" type="QString"/>
                              <Option value="2" name="type" type="int"/>
                            </Option>
                          </Option>
                          <Option value="collection" name="type" type="QString"/>
                        </Option>
                      </data_defined_properties>
                    </layer>
                  </symbol>
                </layer>
              </symbol>
            </layer>
            <layer enabled="1" locked="0" pass="0" class="FontMarker">
              <Option type="Map">
                <Option value="0" name="angle" type="QString"/>
                <Option value="A" name="chr" type="QString"/>
                <Option value="0,0,0,255" name="color" type="QString"/>
                <Option value="Arial" name="font" type="QString"/>
                <Option value="" name="font_style" type="QString"/>
                <Option value="1" name="horizontal_anchor_point" type="QString"/>
                <Option value="miter" name="joinstyle" type="QString"/>
                <Option value="-2,-1" name="offset" type="QString"/>
                <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
                <Option value="MM" name="offset_unit" type="QString"/>
                <Option value="0,0,0,255" name="outline_color" type="QString"/>
                <Option value="0" name="outline_width" type="QString"/>
                <Option value="3x:0,0,0,0,0,0" name="outline_width_map_unit_scale" type="QString"/>
                <Option value="MM" name="outline_width_unit" type="QString"/>
                <Option value="1.8" name="size" type="QString"/>
                <Option value="3x:0,0,0,0,0,0" name="size_map_unit_scale" type="QString"/>
                <Option value="MM" name="size_unit" type="QString"/>
                <Option value="1" name="vertical_anchor_point" type="QString"/>
              </Option>
              <prop v="0" k="angle"/>
              <prop v="A" k="chr"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="Arial" k="font"/>
              <prop v="" k="font_style"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="miter" k="joinstyle"/>
              <prop v="-2,-1" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="0,0,0,255" k="outline_color"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="1.8" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <effect type="effectStack" enabled="1">
                <effect type="dropShadow">
                  <Option type="Map">
                    <Option value="13" name="blend_mode" type="QString"/>
                    <Option value="2.645" name="blur_level" type="QString"/>
                    <Option value="MM" name="blur_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="blur_unit_scale" type="QString"/>
                    <Option value="0,0,0,255" name="color" type="QString"/>
                    <Option value="2" name="draw_mode" type="QString"/>
                    <Option value="0" name="enabled" type="QString"/>
                    <Option value="135" name="offset_angle" type="QString"/>
                    <Option value="2" name="offset_distance" type="QString"/>
                    <Option value="MM" name="offset_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="offset_unit_scale" type="QString"/>
                    <Option value="1" name="opacity" type="QString"/>
                  </Option>
                  <prop v="13" k="blend_mode"/>
                  <prop v="2.645" k="blur_level"/>
                  <prop v="MM" k="blur_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
                  <prop v="0,0,0,255" k="color"/>
                  <prop v="2" k="draw_mode"/>
                  <prop v="0" k="enabled"/>
                  <prop v="135" k="offset_angle"/>
                  <prop v="2" k="offset_distance"/>
                  <prop v="MM" k="offset_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
                  <prop v="1" k="opacity"/>
                </effect>
                <effect type="outerGlow">
                  <Option type="Map">
                    <Option value="0" name="blend_mode" type="QString"/>
                    <Option value="0.2645" name="blur_level" type="QString"/>
                    <Option value="MM" name="blur_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="blur_unit_scale" type="QString"/>
                    <Option value="0,0,255,255" name="color1" type="QString"/>
                    <Option value="0,255,0,255" name="color2" type="QString"/>
                    <Option value="0" name="color_type" type="QString"/>
                    <Option value="0" name="discrete" type="QString"/>
                    <Option value="2" name="draw_mode" type="QString"/>
                    <Option value="1" name="enabled" type="QString"/>
                    <Option value="1" name="opacity" type="QString"/>
                    <Option value="gradient" name="rampType" type="QString"/>
                    <Option value="255,255,255,255" name="single_color" type="QString"/>
                    <Option value="1" name="spread" type="QString"/>
                    <Option value="MM" name="spread_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="spread_unit_scale" type="QString"/>
                  </Option>
                  <prop v="0" k="blend_mode"/>
                  <prop v="0.2645" k="blur_level"/>
                  <prop v="MM" k="blur_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
                  <prop v="0,0,255,255" k="color1"/>
                  <prop v="0,255,0,255" k="color2"/>
                  <prop v="0" k="color_type"/>
                  <prop v="0" k="discrete"/>
                  <prop v="2" k="draw_mode"/>
                  <prop v="1" k="enabled"/>
                  <prop v="1" k="opacity"/>
                  <prop v="gradient" k="rampType"/>
                  <prop v="255,255,255,255" k="single_color"/>
                  <prop v="1" k="spread"/>
                  <prop v="MM" k="spread_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
                </effect>
                <effect type="drawSource">
                  <Option type="Map">
                    <Option value="0" name="blend_mode" type="QString"/>
                    <Option value="2" name="draw_mode" type="QString"/>
                    <Option value="1" name="enabled" type="QString"/>
                    <Option value="1" name="opacity" type="QString"/>
                  </Option>
                  <prop v="0" k="blend_mode"/>
                  <prop v="2" k="draw_mode"/>
                  <prop v="1" k="enabled"/>
                  <prop v="1" k="opacity"/>
                </effect>
                <effect type="innerShadow">
                  <Option type="Map">
                    <Option value="13" name="blend_mode" type="QString"/>
                    <Option value="2.645" name="blur_level" type="QString"/>
                    <Option value="MM" name="blur_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="blur_unit_scale" type="QString"/>
                    <Option value="0,0,0,255" name="color" type="QString"/>
                    <Option value="2" name="draw_mode" type="QString"/>
                    <Option value="0" name="enabled" type="QString"/>
                    <Option value="135" name="offset_angle" type="QString"/>
                    <Option value="2" name="offset_distance" type="QString"/>
                    <Option value="MM" name="offset_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="offset_unit_scale" type="QString"/>
                    <Option value="1" name="opacity" type="QString"/>
                  </Option>
                  <prop v="13" k="blend_mode"/>
                  <prop v="2.645" k="blur_level"/>
                  <prop v="MM" k="blur_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
                  <prop v="0,0,0,255" k="color"/>
                  <prop v="2" k="draw_mode"/>
                  <prop v="0" k="enabled"/>
                  <prop v="135" k="offset_angle"/>
                  <prop v="2" k="offset_distance"/>
                  <prop v="MM" k="offset_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
                  <prop v="1" k="opacity"/>
                </effect>
                <effect type="innerGlow">
                  <Option type="Map">
                    <Option value="0" name="blend_mode" type="QString"/>
                    <Option value="0.7935" name="blur_level" type="QString"/>
                    <Option value="MM" name="blur_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="blur_unit_scale" type="QString"/>
                    <Option value="0,0,255,255" name="color1" type="QString"/>
                    <Option value="0,255,0,255" name="color2" type="QString"/>
                    <Option value="0" name="color_type" type="QString"/>
                    <Option value="0" name="discrete" type="QString"/>
                    <Option value="2" name="draw_mode" type="QString"/>
                    <Option value="0" name="enabled" type="QString"/>
                    <Option value="0.5" name="opacity" type="QString"/>
                    <Option value="gradient" name="rampType" type="QString"/>
                    <Option value="255,255,255,255" name="single_color" type="QString"/>
                    <Option value="2" name="spread" type="QString"/>
                    <Option value="MM" name="spread_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="spread_unit_scale" type="QString"/>
                  </Option>
                  <prop v="0" k="blend_mode"/>
                  <prop v="0.7935" k="blur_level"/>
                  <prop v="MM" k="blur_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
                  <prop v="0,0,255,255" k="color1"/>
                  <prop v="0,255,0,255" k="color2"/>
                  <prop v="0" k="color_type"/>
                  <prop v="0" k="discrete"/>
                  <prop v="2" k="draw_mode"/>
                  <prop v="0" k="enabled"/>
                  <prop v="0.5" k="opacity"/>
                  <prop v="gradient" k="rampType"/>
                  <prop v="255,255,255,255" k="single_color"/>
                  <prop v="2" k="spread"/>
                  <prop v="MM" k="spread_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
                </effect>
              </effect>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="char" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="'Y = ' || round(x(&#xd;&#xa;&#x9;point_n($geometry, @geometry_part_num)&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;3&#xd;&#xa;)" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                    <Option name="offset" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="CASE WHEN degrees(&#xd;&#xa;&#x9;azimuth(centroid($geometry), point_n($geometry, @geometry_part_num))&#xd;&#xa;&#x9;) &lt; 90 THEN '6.0000, -7.0000'&#xd;&#xa;&#x9;WHEN degrees(&#xd;&#xa;&#x9;azimuth(centroid($geometry), point_n($geometry, @geometry_part_num))&#xd;&#xa;&#x9;) &lt; 180 THEN '6.0000, 4.0000'&#xd;&#xa;&#x9;WHEN degrees(&#xd;&#xa;&#x9;azimuth(centroid($geometry), point_n($geometry, @geometry_part_num))&#xd;&#xa;&#x9;) &lt; 270 THEN '-5.8000, 4.0000'&#xd;&#xa;ELSE&#xd;&#xa;&#x9;'-5.8000, -7.0000'&#xd;&#xa;END" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                  </Option>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
            <layer enabled="1" locked="0" pass="0" class="FontMarker">
              <Option type="Map">
                <Option value="0" name="angle" type="QString"/>
                <Option value="A" name="chr" type="QString"/>
                <Option value="0,0,0,255" name="color" type="QString"/>
                <Option value="Arial" name="font" type="QString"/>
                <Option value="" name="font_style" type="QString"/>
                <Option value="1" name="horizontal_anchor_point" type="QString"/>
                <Option value="bevel" name="joinstyle" type="QString"/>
                <Option value="-2,-1" name="offset" type="QString"/>
                <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
                <Option value="MM" name="offset_unit" type="QString"/>
                <Option value="166,206,227,255" name="outline_color" type="QString"/>
                <Option value="0" name="outline_width" type="QString"/>
                <Option value="3x:0,0,0,0,0,0" name="outline_width_map_unit_scale" type="QString"/>
                <Option value="MM" name="outline_width_unit" type="QString"/>
                <Option value="1.8" name="size" type="QString"/>
                <Option value="3x:0,0,0,0,0,0" name="size_map_unit_scale" type="QString"/>
                <Option value="MM" name="size_unit" type="QString"/>
                <Option value="1" name="vertical_anchor_point" type="QString"/>
              </Option>
              <prop v="0" k="angle"/>
              <prop v="A" k="chr"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="Arial" k="font"/>
              <prop v="" k="font_style"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="-2,-1" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="166,206,227,255" k="outline_color"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="1.8" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <effect type="effectStack" enabled="1">
                <effect type="dropShadow">
                  <Option type="Map">
                    <Option value="13" name="blend_mode" type="QString"/>
                    <Option value="2.645" name="blur_level" type="QString"/>
                    <Option value="MM" name="blur_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="blur_unit_scale" type="QString"/>
                    <Option value="0,0,0,255" name="color" type="QString"/>
                    <Option value="2" name="draw_mode" type="QString"/>
                    <Option value="0" name="enabled" type="QString"/>
                    <Option value="135" name="offset_angle" type="QString"/>
                    <Option value="2" name="offset_distance" type="QString"/>
                    <Option value="MM" name="offset_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="offset_unit_scale" type="QString"/>
                    <Option value="1" name="opacity" type="QString"/>
                  </Option>
                  <prop v="13" k="blend_mode"/>
                  <prop v="2.645" k="blur_level"/>
                  <prop v="MM" k="blur_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
                  <prop v="0,0,0,255" k="color"/>
                  <prop v="2" k="draw_mode"/>
                  <prop v="0" k="enabled"/>
                  <prop v="135" k="offset_angle"/>
                  <prop v="2" k="offset_distance"/>
                  <prop v="MM" k="offset_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
                  <prop v="1" k="opacity"/>
                </effect>
                <effect type="outerGlow">
                  <Option type="Map">
                    <Option value="0" name="blend_mode" type="QString"/>
                    <Option value="0.2645" name="blur_level" type="QString"/>
                    <Option value="MM" name="blur_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="blur_unit_scale" type="QString"/>
                    <Option value="255,255,255,255" name="color1" type="QString"/>
                    <Option value="207,209,213,255" name="color2" type="QString"/>
                    <Option value="0" name="color_type" type="QString"/>
                    <Option value="0" name="discrete" type="QString"/>
                    <Option value="2" name="draw_mode" type="QString"/>
                    <Option value="1" name="enabled" type="QString"/>
                    <Option value="1" name="opacity" type="QString"/>
                    <Option value="gradient" name="rampType" type="QString"/>
                    <Option value="255,255,255,255" name="single_color" type="QString"/>
                    <Option value="1" name="spread" type="QString"/>
                    <Option value="MM" name="spread_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="spread_unit_scale" type="QString"/>
                  </Option>
                  <prop v="0" k="blend_mode"/>
                  <prop v="0.2645" k="blur_level"/>
                  <prop v="MM" k="blur_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
                  <prop v="255,255,255,255" k="color1"/>
                  <prop v="207,209,213,255" k="color2"/>
                  <prop v="0" k="color_type"/>
                  <prop v="0" k="discrete"/>
                  <prop v="2" k="draw_mode"/>
                  <prop v="1" k="enabled"/>
                  <prop v="1" k="opacity"/>
                  <prop v="gradient" k="rampType"/>
                  <prop v="255,255,255,255" k="single_color"/>
                  <prop v="1" k="spread"/>
                  <prop v="MM" k="spread_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
                </effect>
                <effect type="drawSource">
                  <Option type="Map">
                    <Option value="0" name="blend_mode" type="QString"/>
                    <Option value="2" name="draw_mode" type="QString"/>
                    <Option value="1" name="enabled" type="QString"/>
                    <Option value="1" name="opacity" type="QString"/>
                  </Option>
                  <prop v="0" k="blend_mode"/>
                  <prop v="2" k="draw_mode"/>
                  <prop v="1" k="enabled"/>
                  <prop v="1" k="opacity"/>
                </effect>
                <effect type="innerShadow">
                  <Option type="Map">
                    <Option value="13" name="blend_mode" type="QString"/>
                    <Option value="2.645" name="blur_level" type="QString"/>
                    <Option value="MM" name="blur_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="blur_unit_scale" type="QString"/>
                    <Option value="0,0,0,255" name="color" type="QString"/>
                    <Option value="2" name="draw_mode" type="QString"/>
                    <Option value="0" name="enabled" type="QString"/>
                    <Option value="135" name="offset_angle" type="QString"/>
                    <Option value="2" name="offset_distance" type="QString"/>
                    <Option value="MM" name="offset_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="offset_unit_scale" type="QString"/>
                    <Option value="1" name="opacity" type="QString"/>
                  </Option>
                  <prop v="13" k="blend_mode"/>
                  <prop v="2.645" k="blur_level"/>
                  <prop v="MM" k="blur_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
                  <prop v="0,0,0,255" k="color"/>
                  <prop v="2" k="draw_mode"/>
                  <prop v="0" k="enabled"/>
                  <prop v="135" k="offset_angle"/>
                  <prop v="2" k="offset_distance"/>
                  <prop v="MM" k="offset_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
                  <prop v="1" k="opacity"/>
                </effect>
                <effect type="innerGlow">
                  <Option type="Map">
                    <Option value="0" name="blend_mode" type="QString"/>
                    <Option value="0.7935" name="blur_level" type="QString"/>
                    <Option value="MM" name="blur_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="blur_unit_scale" type="QString"/>
                    <Option value="0,0,255,255" name="color1" type="QString"/>
                    <Option value="0,255,0,255" name="color2" type="QString"/>
                    <Option value="0" name="color_type" type="QString"/>
                    <Option value="0" name="discrete" type="QString"/>
                    <Option value="2" name="draw_mode" type="QString"/>
                    <Option value="0" name="enabled" type="QString"/>
                    <Option value="0.5" name="opacity" type="QString"/>
                    <Option value="gradient" name="rampType" type="QString"/>
                    <Option value="255,255,255,255" name="single_color" type="QString"/>
                    <Option value="2" name="spread" type="QString"/>
                    <Option value="MM" name="spread_unit" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="spread_unit_scale" type="QString"/>
                  </Option>
                  <prop v="0" k="blend_mode"/>
                  <prop v="0.7935" k="blur_level"/>
                  <prop v="MM" k="blur_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
                  <prop v="0,0,255,255" k="color1"/>
                  <prop v="0,255,0,255" k="color2"/>
                  <prop v="0" k="color_type"/>
                  <prop v="0" k="discrete"/>
                  <prop v="2" k="draw_mode"/>
                  <prop v="0" k="enabled"/>
                  <prop v="0.5" k="opacity"/>
                  <prop v="gradient" k="rampType"/>
                  <prop v="255,255,255,255" k="single_color"/>
                  <prop v="2" k="spread"/>
                  <prop v="MM" k="spread_unit"/>
                  <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
                </effect>
              </effect>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="char" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="'X = ' || round(y(&#xd;&#xa;&#x9;point_n($geometry, @geometry_part_num)&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;3&#xd;&#xa;)" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                    <Option name="offset" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="CASE WHEN degrees(&#xd;&#xa;&#x9;azimuth(centroid($geometry), point_n($geometry, @geometry_part_num))&#xd;&#xa;&#x9;) &lt; 90 THEN '6.5000, -4.8000'&#xd;&#xa;&#x9;WHEN degrees(&#xd;&#xa;&#x9;azimuth(centroid($geometry), point_n($geometry, @geometry_part_num))&#xd;&#xa;&#x9;) &lt; 180 THEN '6.3000, 6.2000'&#xd;&#xa;&#x9;WHEN degrees(&#xd;&#xa;&#x9;azimuth(centroid($geometry), point_n($geometry, @geometry_part_num))&#xd;&#xa;&#x9;) &lt; 270 THEN '-5.2000, 6.2000'&#xd;&#xa;ELSE&#xd;&#xa;&#x9;'-5.0000, -4.3000'&#xd;&#xa;END" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                  </Option>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <Option type="Map">
      <Option value="0" name="embeddedWidgets/count" type="QString"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory maxScaleDenominator="1e+08" backgroundColor="#ffffff" rotationOffset="270" sizeScale="3x:0,0,0,0,0,0" penColor="#000000" width="15" backgroundAlpha="255" minimumSize="0" spacing="0" minScaleDenominator="0" showAxis="0" opacity="1" lineSizeType="MM" scaleBasedVisibility="0" scaleDependency="Area" height="15" sizeType="MM" barWidth="5" spacingUnitScale="3x:0,0,0,0,0,0" diagramOrientation="Up" enabled="0" spacingUnit="MM" penAlpha="255" direction="1" lineSizeScale="3x:0,0,0,0,0,0" penWidth="0" labelPlacementMethod="XHeight">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" field="" color="#000000"/>
      <axisSymbol>
        <symbol name="" type="line" force_rhr="0" clip_to_extent="1" alpha="1">
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <layer enabled="1" locked="0" pass="0" class="SimpleLine">
            <Option type="Map">
              <Option value="0" name="align_dash_pattern" type="QString"/>
              <Option value="square" name="capstyle" type="QString"/>
              <Option value="5;2" name="customdash" type="QString"/>
              <Option value="3x:0,0,0,0,0,0" name="customdash_map_unit_scale" type="QString"/>
              <Option value="MM" name="customdash_unit" type="QString"/>
              <Option value="0" name="dash_pattern_offset" type="QString"/>
              <Option value="3x:0,0,0,0,0,0" name="dash_pattern_offset_map_unit_scale" type="QString"/>
              <Option value="MM" name="dash_pattern_offset_unit" type="QString"/>
              <Option value="0" name="draw_inside_polygon" type="QString"/>
              <Option value="bevel" name="joinstyle" type="QString"/>
              <Option value="35,35,35,255" name="line_color" type="QString"/>
              <Option value="solid" name="line_style" type="QString"/>
              <Option value="0.26" name="line_width" type="QString"/>
              <Option value="MM" name="line_width_unit" type="QString"/>
              <Option value="0" name="offset" type="QString"/>
              <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
              <Option value="MM" name="offset_unit" type="QString"/>
              <Option value="0" name="ring_filter" type="QString"/>
              <Option value="0" name="trim_distance_end" type="QString"/>
              <Option value="3x:0,0,0,0,0,0" name="trim_distance_end_map_unit_scale" type="QString"/>
              <Option value="MM" name="trim_distance_end_unit" type="QString"/>
              <Option value="0" name="trim_distance_start" type="QString"/>
              <Option value="3x:0,0,0,0,0,0" name="trim_distance_start_map_unit_scale" type="QString"/>
              <Option value="MM" name="trim_distance_start_unit" type="QString"/>
              <Option value="0" name="tweak_dash_pattern_on_corners" type="QString"/>
              <Option value="0" name="use_custom_dash" type="QString"/>
              <Option value="3x:0,0,0,0,0,0" name="width_map_unit_scale" type="QString"/>
            </Option>
            <prop v="0" k="align_dash_pattern"/>
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="dash_pattern_offset"/>
            <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
            <prop v="MM" k="dash_pattern_offset_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
            <prop v="MM" k="line_width_unit"/>
            <prop v="0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="0" k="ring_filter"/>
            <prop v="0" k="trim_distance_end"/>
            <prop v="3x:0,0,0,0,0,0" k="trim_distance_end_map_unit_scale"/>
            <prop v="MM" k="trim_distance_end_unit"/>
            <prop v="0" k="trim_distance_start"/>
            <prop v="3x:0,0,0,0,0,0" k="trim_distance_start_map_unit_scale"/>
            <prop v="MM" k="trim_distance_start_unit"/>
            <prop v="0" k="tweak_dash_pattern_on_corners"/>
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" dist="0" placement="0" priority="0" linePlacementFlags="2" showAll="1" obstacle="0">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option name="QgsGeometryGapCheck" type="Map">
        <Option value="0" name="allowedGapsBuffer" type="double"/>
        <Option value="false" name="allowedGapsEnabled" type="bool"/>
        <Option value="" name="allowedGapsLayer" type="QString"/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <legend type="default-vector" showLabelLegend="0"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="plot_number" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="area" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="scheme_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="use_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="crs_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="imposing_condition_number" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="transfer_contract_number" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="holder_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="transfer_contract_date" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="id" index="0"/>
    <alias name="" field="plot_number" index="1"/>
    <alias name="" field="area" index="2"/>
    <alias name="" field="scheme_id" index="3"/>
    <alias name="" field="use_id" index="4"/>
    <alias name="" field="crs_id" index="5"/>
    <alias name="" field="imposing_condition_number" index="6"/>
    <alias name="" field="transfer_contract_number" index="7"/>
    <alias name="" field="holder_id" index="8"/>
    <alias name="" field="transfer_contract_date" index="9"/>
  </aliases>
  <defaults>
    <default expression="" field="id" applyOnUpdate="0"/>
    <default expression="" field="plot_number" applyOnUpdate="0"/>
    <default expression="" field="area" applyOnUpdate="0"/>
    <default expression="" field="scheme_id" applyOnUpdate="0"/>
    <default expression="" field="use_id" applyOnUpdate="0"/>
    <default expression="" field="crs_id" applyOnUpdate="0"/>
    <default expression="" field="imposing_condition_number" applyOnUpdate="0"/>
    <default expression="" field="transfer_contract_number" applyOnUpdate="0"/>
    <default expression="" field="holder_id" applyOnUpdate="0"/>
    <default expression="" field="transfer_contract_date" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint constraints="3" field="id" notnull_strength="1" unique_strength="1" exp_strength="0"/>
    <constraint constraints="1" field="plot_number" notnull_strength="1" unique_strength="0" exp_strength="0"/>
    <constraint constraints="0" field="area" notnull_strength="0" unique_strength="0" exp_strength="0"/>
    <constraint constraints="0" field="scheme_id" notnull_strength="0" unique_strength="0" exp_strength="0"/>
    <constraint constraints="0" field="use_id" notnull_strength="0" unique_strength="0" exp_strength="0"/>
    <constraint constraints="0" field="crs_id" notnull_strength="0" unique_strength="0" exp_strength="0"/>
    <constraint constraints="0" field="imposing_condition_number" notnull_strength="0" unique_strength="0" exp_strength="0"/>
    <constraint constraints="0" field="transfer_contract_number" notnull_strength="0" unique_strength="0" exp_strength="0"/>
    <constraint constraints="0" field="holder_id" notnull_strength="0" unique_strength="0" exp_strength="0"/>
    <constraint constraints="0" field="transfer_contract_date" notnull_strength="0" unique_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="plot_number"/>
    <constraint exp="" desc="" field="area"/>
    <constraint exp="" desc="" field="scheme_id"/>
    <constraint exp="" desc="" field="use_id"/>
    <constraint exp="" desc="" field="crs_id"/>
    <constraint exp="" desc="" field="imposing_condition_number"/>
    <constraint exp="" desc="" field="transfer_contract_number"/>
    <constraint exp="" desc="" field="holder_id"/>
    <constraint exp="" desc="" field="transfer_contract_date"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column type="actions" width="-1" hidden="1"/>
      <column name="id" type="field" width="-1" hidden="0"/>
      <column name="area" type="field" width="-1" hidden="0"/>
      <column name="scheme_id" type="field" width="-1" hidden="0"/>
      <column name="plot_number" type="field" width="-1" hidden="0"/>
      <column name="use_id" type="field" width="-1" hidden="0"/>
      <column name="imposing_condition_number" type="field" width="-1" hidden="0"/>
      <column name="transfer_contract_number" type="field" width="-1" hidden="0"/>
      <column name="holder_id" type="field" width="-1" hidden="0"/>
      <column name="transfer_contract_date" type="field" width="-1" hidden="0"/>
      <column name="crs_id" type="field" width="-1" hidden="0"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">.</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="area"/>
    <field editable="1" name="crs_id"/>
    <field editable="1" name="holder_id"/>
    <field editable="1" name="id"/>
    <field editable="1" name="imposing_condition_number"/>
    <field editable="1" name="plot_number"/>
    <field editable="1" name="scheme_id"/>
    <field editable="1" name="transfer_contract_date"/>
    <field editable="1" name="transfer_contract_number"/>
    <field editable="1" name="use_id"/>
  </editable>
  <labelOnTop>
    <field name="area" labelOnTop="0"/>
    <field name="crs_id" labelOnTop="0"/>
    <field name="holder_id" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="imposing_condition_number" labelOnTop="0"/>
    <field name="plot_number" labelOnTop="0"/>
    <field name="scheme_id" labelOnTop="0"/>
    <field name="transfer_contract_date" labelOnTop="0"/>
    <field name="transfer_contract_number" labelOnTop="0"/>
    <field name="use_id" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field reuseLastValue="0" name="area"/>
    <field reuseLastValue="0" name="crs_id"/>
    <field reuseLastValue="0" name="holder_id"/>
    <field reuseLastValue="0" name="id"/>
    <field reuseLastValue="0" name="imposing_condition_number"/>
    <field reuseLastValue="0" name="plot_number"/>
    <field reuseLastValue="0" name="scheme_id"/>
    <field reuseLastValue="0" name="transfer_contract_date"/>
    <field reuseLastValue="0" name="transfer_contract_number"/>
    <field reuseLastValue="0" name="use_id"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
