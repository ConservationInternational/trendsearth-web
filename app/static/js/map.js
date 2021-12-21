const drawMap = function (mapDiv) {
  var mainView = new ol.View({
    center: [0, 0],
    minZoom: 1,
    maxZoom: 20,
    zoom: 3,
  });

  const mainMap = new ol.Map({
    controls: [],
    target: mapDiv,
    view: mainView,
  });

  var base_urls = [
    {
      url: "https://api.mapbox.com/styles/v1/cigrp/cixkh6jb000582smx8pfdeu23/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiY2lncnAiLCJhIjoiYTQ5YzVmYTk4YzM0ZWM4OTU1ZjQxMWI5ZDNiNTQ5M2IifQ.SBgo9jJftBDx4c5gX4wm3g",
      visible: true,
    },
    {
      url: "https://api.mapbox.com/styles/v1/cigrp/cizsz6pv700422ro73xdhzi1g/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiY2lncnAiLCJhIjoiYTQ5YzVmYTk4YzM0ZWM4OTU1ZjQxMWI5ZDNiNTQ5M2IifQ.SBgo9jJftBDx4c5gX4wm3g",
      visible: false,
    },
    {
      url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}",
      visible: false,
    },
    {
      url: "https://api.mapbox.com/styles/v1/cigrp/cixtef50400162rla1jtwtoyi/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiY2lncnAiLCJhIjoiYTQ5YzVmYTk4YzM0ZWM4OTU1ZjQxMWI5ZDNiNTQ5M2IifQ.SBgo9jJftBDx4c5gX4wm3g",
      visible: false,
    },
  ];

  var baseLayers = [];
  base_urls.forEach((element) => {
    baseLayers.push(
      new ol.layer.Tile({
        name: "Base Map",
        source: new ol.source.TileImage({
          url: element.url,
        }),
        visible: element.visible == 1,
        opacity: 1,
      })
    );
  });

  const baseLayerGroup = new ol.layer.Group({
    layers: baseLayers,
    id: "base_layers",
    visible: true,
  });

  mainMap.addLayer(baseLayerGroup);

  mainMap.on("pointermove", (evt) => {
    if (evt.dragging) {
      return;
    }
    var coord3857 = evt.coordinate;
    var coord4326 = ol.proj.transform(coord3857, "EPSG:3857", "EPSG:4326");
    document.getElementById("lat").innerHTML = "Lat " + coord4326[1].toFixed(3);
    document.getElementById("lon").innerHTML = "Lon " + coord4326[0].toFixed(3);
  });

  $("#dropdownZoomIn").on("click", function () {
    var view = mainMap.getView();
    mainMap.getView().animate({ zoom: view.getZoom() + 1 });
  });

  $("#dropdownZoomOut").on("click", function () {
    var view = mainMap.getView();
    mainMap.getView().animate({ zoom: view.getZoom() - 1 });
  });

  $(".m-basemap-selectors button").on("click", function () {
    $(".m-basemap-selectors button").removeClass("is-active");
    let id = +$(this).attr("id").split("-")[1];
    for (var i = 0; i < base_urls.length; i++) {
      if (i == id) {
        $(this).addClass("is-active");
        baseLayerGroup.getLayers().getArray()[i].setVisible(true);
      } else {
        baseLayerGroup.getLayers().getArray()[i].setVisible(false);
      }
    }
  });
  $("#layers_panel").hide();
  $("#btnLayers").on("click", function () {
    $("#layers_panel").toggle();
  });

  $("#btn_close_layers_panel").on("click", function () {
    $("#layers_panel").hide();
  });
  return mainMap;
};
