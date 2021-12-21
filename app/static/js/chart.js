const drawLineChart = function (
  data,
  {
    x = ([x]) => x,
    y = ([, y]) => y,
    z = () => 1,
    code,
    title,
    defined,
    curve = d3.curveLinear,
    marginTop = 20,
    marginRight = 30,
    marginBottom = 30,
    marginLeft = 40,
    width = 640,
    height = 400,
    xType = d3.scaleUtc, // type of x-scale
    xDomain, // [xmin, xmax]
    xRange = [marginLeft, width - marginRight], // [left, right]
    yType = d3.scaleLinear, // type of y-scale
    yDomain, // [ymin, ymax]
    yRange = [height - marginBottom, marginTop], // [bottom, top]
    yFormat, // a format specifier string for the y-axis
    yLabel, // a label for the y-axis
    zDomain, // array of z-values
    color = "currentColor", // stroke color of line, as a constant or a function of *z*
    strokeLinecap, // stroke line cap of line
    strokeLinejoin, // stroke line join of line
    strokeWidth = 1.5, // stroke width of line
    strokeOpacity, // stroke opacity of line
    mixBlendMode = "multiply", // blend mode of lines
    voronoi, // show a Voronoi overlay? (for debugging)
    targetPanel = "line_chart",
  } = {}
) {
  if (data.length == 0) {
    $("#" + targetPanel).append("<p>No Data</p>");
    return;
  }

  $("#" + targetPanel).empty();

  // Compute values.
  const X = d3.map(data, x);
  const Y = d3.map(data, y);
  const Z = d3.map(data, z);
  const Code = d3.map(data, code);
  const O = d3.map(data, (d) => d);
  if (defined === undefined) defined = (d, i) => !isNaN(X[i]) && !isNaN(Y[i]);
  const D = d3.map(data, defined);

  // var colors = d3.schemeTableau10;

  // Compute default domains, and unique the z-domain.
  if (xDomain === undefined) xDomain = d3.extent(X);
  if (yDomain === undefined) yDomain = [0, d3.max(Y)];
  if (zDomain === undefined) zDomain = Z;
  zDomain = new d3.InternSet(zDomain);

  // color = d3.scaleOrdinal(zDomain, colors);

  // Omit any data not present in the z-domain.
  const I = d3.range(X.length).filter((i) => zDomain.has(Z[i]));

  // Construct scales and axes.
  const xScale = xType(xDomain, xRange);
  const yScale = yType(yDomain, yRange);
  const xAxis = d3
    .axisBottom(xScale)
    .ticks(width / 80)
    .tickSizeOuter(0);
  const yAxis = d3.axisLeft(yScale).ticks(height / 60, yFormat);

  // Compute titles.
  const T =
    title === undefined ? Z : title === null ? null : d3.map(data, title);

  // Construct a line generator.
  const line = d3
    .line()
    .defined((i) => D[i])
    .curve(curve)
    .x((i) => xScale(X[i]))
    .y((i) => yScale(Y[i]));

  const svg = d3
    .select("#" + targetPanel)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "max-width: 100%; height: auto; height: intrinsic;")
    .style("-webkit-tap-highlight-color", "transparent")
    .on("pointerenter", pointerentered)
    .on("pointermove", pointermoved)
    .on("pointerleave", pointerleft)
    .on("touchstart", (event) => event.preventDefault());

  // An optional Voronoi display (for fun).
  if (voronoi)
    svg
      .append("path")
      .attr("fill", "none")
      .attr("stroke", "#ccc")
      .attr(
        "d",
        d3.Delaunay.from(
          I,
          (i) => xScale(X[i]),
          (i) => yScale(Y[i])
        )
          .voronoi([0, 0, width, height])
          .render()
      );

  svg
    .append("g")
    .attr("transform", `translate(0,${height - marginBottom})`)
    .call(xAxis);

  svg
    .append("g")
    .attr("transform", `translate(${marginLeft},0)`)
    .call(yAxis)
    .call((g) => g.select(".domain").remove())
    .call(
      voronoi
        ? () => {}
        : (g) =>
            g
              .selectAll(".tick line")
              .clone()
              .attr("x2", width - marginLeft - marginRight)
              .attr("stroke-opacity", 0.1)
    )
    .call((g) =>
      g
        .append("text")
        .attr("x", -marginLeft)
        .attr("y", 10)
        .attr("fill", "currentColor")
        .attr("text-anchor", "start")
        .text(yLabel)
    );

  const path = svg
    .append("g")
    .attr("fill", "none")
    .attr("stroke", typeof color === "string" ? color : null)
    .attr("stroke-linecap", strokeLinecap)
    .attr("stroke-linejoin", strokeLinejoin)
    .attr("stroke-width", strokeWidth)
    .attr("stroke-opacity", strokeOpacity)
    .selectAll("path")
    .data(d3.group(I, (i) => Z[i]))
    .join("path")
    .style("mix-blend-mode", mixBlendMode)
    .attr("stroke", typeof color === "function" ? ([z]) => color(z) : null)
    .attr("d", ([, I]) => line(I))
    .attr("class", "line-element")
    .attr("id", (d) => "line-" + d.code);

  const dot = svg.append("g").attr("display", "none");

  dot.append("circle").attr("r", 2.5);

  dot
    .append("text")
    .attr("font-family", "sans-serif")
    .attr("font-size", 10)
    .attr("text-anchor", "middle")
    .attr("y", -8);

  function pointermoved(event) {
    const [xm, ym] = d3.pointer(event);
    const i = d3.least(I, (i) =>
      Math.hypot(xScale(X[i]) - xm, yScale(Y[i]) - ym)
    );
    path
      .style("stroke", ([z]) => (Z[i] === z ? null : "#ddd"))
      .filter(([z]) => Z[i] === z)
      .raise();
    dot.attr("transform", `translate(${xScale(X[i])},${yScale(Y[i])})`);
    if (T) dot.select("text").text(T[i]);
    svg.property("value", O[i]).dispatch("input", { bubbles: true });
    d3.selectAll(".legend-element").style("opacity", function (r) {
      return r.code == Code[i] ? 1 : 0.2;
    });

    d3.selectAll(".pie-element").style("opacity", function (r) {
      console.log(r);
      return r.data.code == Code[i] ? 1 : 0.2;
    });
  }

  function pointerentered() {
    path.style("mix-blend-mode", null).style("stroke", "#ddd");
    dot.attr("display", null);
  }

  function pointerleft() {
    path.style("mix-blend-mode", "multiply").style("stroke", null);
    dot.attr("display", "none");
    svg.node().value = null;
    svg.dispatch("input", { bubbles: true });
    d3.selectAll(".legend-element").style("opacity", 1);
    d3.selectAll(".pie-element").style("opacity", 1);
  }

  return Object.assign(svg.node(), { value: null });
};

const drawPieChart = function (data, color, targetpanel, height) {
  if (data.length == 0) {
    $("#" + targetpanel).append("<p>No Data</p>");
    return;
  }

  $("#" + targetpanel).empty();
  /*---*/
  function onMouseoverPie(event, slice) {
    d3.selectAll(".legend-element").style("opacity", function (r) {
      return r.code == slice.data.code ? 1 : 0.2;
    });

    d3.selectAll(".line-element").style("opacity", function (r) {
      return r[0] == slice.data.group ? 1 : 0.2;
    });
  }

  function onMouseoutPie() {
    d3.selectAll(".legend-element").style("opacity", 1);
    d3.selectAll(".line-element").style("opacity", 1);
  }
  /*---*/

  var pc = new Object();

  var keys, total;
  var total = d3.sum(data, function (r) {
    return r.value;
  });

  keys = data.map(function (r) {
    return r.name;
  });

  pc.data = data.map(function (r) {
    return {
      group: r.name,
      value: r.value,
      code: r.code,
      pct: Math.round((r.value / total) * 100),
    };
  });

  /* Pie chart margins and dimensions */
  pc.width = $("#" + targetpanel).width();
  pc.height = height;
  pc.radius = Math.min(pc.width, pc.height) / 2;

  /* Pie chart object */
  pc.obj = d3
    .select("#" + targetpanel)
    .append("svg")
    .attr("width", pc.width)
    .attr("height", pc.height)
    .attr("id", "pie_chart")
    .append("g")
    .attr(
      "transform",
      "translate(" + pc.width / 2 + "," + (pc.height / 2 - 10) + ")"
    );

  /* Arc & slice functions */
  pc.arc = d3
    .arc()
    .outerRadius(pc.radius - 15)
    .innerRadius(0);

  pc.slice = d3
    .pie()
    .sort(null)
    .value(function (r) {
      return r.value;
    });
  /* Pie slices */
  pc.obj
    .selectAll("path")
    .data(pc.slice(pc.data))
    .enter()
    .append("path")
    .attr("id", function (r) {
      return "pie_" + r.data.code;
    })
    .attr("class", "pie-element")
    .attr("d", pc.arc)
    .style("fill-opacity", 1)
    .style("fill", function (r) {
      return color(r.data.group);
    })
    .style("stroke", "#fff")
    .style("stroke-width", 1)
    .attr("stroke-linejoin", "round")
    .on("mouseover", onMouseoverPie)
    .on("mouseout", onMouseoutPie);

  /* Pie Title */
  pc.obj
    .append("text")
    .attr("id", "pie_title")
    .attr("x", 0)
    .attr("y", 147)
    .style("font-size", "13px")
    .style("text-anchor", "middle")
    .text("Summary of usage");

  /* Labels for the various pie slices */
  pc.labelArc = d3
    .arc()
    .outerRadius(pc.radius + 140)
    .innerRadius(0);

  pc.labelAngle = function (r) {
    var a = ((r.startAngle + r.endAngle) * 90) / Math.PI - 90;
    return a > 90 ? a - 180 : a;
  };

  pc.obj
    .selectAll(".pie-label")
    .data(pc.slice(pc.data))
    .enter()
    .append("text")
    .attr("class", "pie-label")
    .attr("text-anchor", "middle")
    .attr("dy", ".35em")
    .attr("transform", function (r) {
      return (
        "translate(" +
        pc.labelArc.centroid(r) +
        ")rotate(" +
        pc.labelAngle(r) +
        ")"
      );
    })
    .text(function (r) {
      return r.data.pct > 0.9 ? r.data.pct + "%" : "";
    });

  /* Animation function */
  pc.sliceTween = function (r) {
    var i = d3.interpolate(this._current, r);
    this._current = i(0);
    return function (t) {
      return pc.arc(i(t));
    };
  };
};

const drawPieLegend = function (data, color, targetPanel) {
  if (data.length == 0) {
    return;
  }

  $("#" + targetPanel).empty();

  var lg = new Object();
  lg.panel = $("#" + targetPanel);

  lg.width = lg.panel.width();
  lg.height = 50 * data.length;

  /* Legend object */
  lg.obj = d3
    .select("#" + targetPanel)
    .append("svg")
    .attr("id", "pie_legend")
    .attr("width", lg.width)
    .attr("height", lg.height)
    .attr("viewBox", [0, 0, lg.width, lg.height]);

  var square = 28;
  var top = 50;

  /* Containers for each legend item */
  lg.obj
    .selectAll(".legend-element")
    .data(data)
    .enter()
    .append("g")
    .attr("id", function (r) {
      return r.code;
    })
    .attr("class", "legend-element")
    .attr("transform", function (r, i) {
      var x = 5;
      var y = i * square + top;
      return "translate(" + x + "," + y + ")";
    });

  /* Color squares */
  lg.obj
    .selectAll(".legend-element")
    .append("rect")
    .attr("width", square / 2)
    .attr("height", square / 2)
    .style("fill-opacity", 0.9)
    .style("fill", function (r) {
      return color(r.name);
    })
    .style("stroke", "#fff");

  /* Legend labels */
  lg.obj
    .selectAll(".legend-element")
    .append("text")
    .attr("x", 20)
    .attr("y", 12)
    .style("font-weight", 400)
    .text(function (r) {
      return r.name;
    });

  /* Legend title */
  lg.obj
    .append("text")
    .attr("x", 5)
    .attr("y", top - 15)
    .style("font-size", "13px")
    .style("font-weight", "500")
    .style("text-anchor", "start")
    .text("Algorithm Classes");
};
