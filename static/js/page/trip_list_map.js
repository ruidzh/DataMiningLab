require(['jquery',google_map_api,'gmap3'], function($){
    var cluster, marker;
    function initMaps() {
            list_map = {
                add: function (columndata) { //data from datatables
                    var self = this;
                    this.map.cluster({
                        size: 150,
                        markers: points2positions(columndata),
                        cb: function (markers) {
                            if (markers.length > 1) { // 1 marker stay unchanged (because cb returns nothing)
                                if (markers.length < 20) {
                                    return {
                                    content: "<div class='cluster cluster-1'>" + markers.length + "</div>",
                                    x: -26,
                                    y: -26
                                    };
                                }
                                if (markers.length < 50) {
                                    return {
                                    content: "<div class='cluster cluster-2'>" + markers.length + "</div>",
                                    x: -26,
                                    y: -26
                                    };
                                }
                                return {
                                    content: "<div class='cluster cluster-3'>" + markers.length + "</div>",
                                    x: -33,
                                    y: -33
                                };
                            }
                        }
                    })
                    .then(function (_cluster) {
                        self.cluster = _cluster;
                    });
                },
                clear: function () {
                    if (this.cluster) {//created
                        var cluster = this.cluster 
                        cluster.filter(function(marker){
                            cluster.remove(marker);
                            marker.setMap(null);
                            return true;
                        });
                    }
                },
                draw: function () {
                    this.clear();
                    if ($('#map_pickup').is(":checked")) {
                        if ($('#map_dropoff').is(":checked")) {
                            this.add(columndata_dropoff.concat(columndata_pickup));
                        } else {
                            this.add(columndata_pickup);
                        }
                    } else if ($('#map_dropoff').is(":checked")) {
                        this.add(columndata_dropoff);
                    }
                    this.map.fit();
                }
            };
            list_map.map = $('#list_map').gmap3({
                    //key: "AIzaSyBR7Z6npapsj4l93EOv6awYTALsvvr-EZs",
                    center: {
                        lat: 40.7625,
                        lng: -73.9742
                    },
                    zoom: 7,
                    mapTypeId : google.maps.MapTypeId.ROADMAP
                }).then(
                    function(_map) {
                        tripstable.on( 'draw', function () {
                            columndata_pickup = tripstable.columns(1).data().toArray().join(); // Reduce the 2D array into a 1D array of data
                            columndata_dropoff = tripstable.columns(2).data().toArray().join(); // Reduce the 2D array into a 1D array of data
                            list_map.draw();
                        } );
                    }
                );

            single_map = {
                show: function (rowData) { //data from datatables
                    var self = this;
                    this.map.route({
                        origin:rowData.pickup,
                        destination:rowData.dropoff,
                        travelMode: google.maps.DirectionsTravelMode.DRIVING
                    })
                    .directionsrenderer(function (results) {
                        if (results) {
                            return {
                                directions: results
                                }
                        }
                    });
                },
                draw: function () {
                    this.show(singleData);
                    this.map.fit();
                }
            };
            single_map.map = $('#single_map').gmap3({
                    //key: "AIzaSyBR7Z6npapsj4l93EOv6awYTALsvvr-EZs",
                    center: {
                        lat: 40.7625,
                        lng: -73.9742
                    },
                    zoom: 7,
                    mapTypeId : google.maps.MapTypeId.ROADMAP
                })      
                .then(function (map) {
                    document.getElementById("single-map").className = "tab-pane fade";
                    $('#map_panel').collapse();
                });
        }
        initMaps();
    });    