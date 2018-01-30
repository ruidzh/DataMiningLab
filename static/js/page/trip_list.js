function point2lnglat(str) {
    var numberPattern = /[+-]?\d+(\.\d+)?/g;
    num = str.match( numberPattern ).map(function(v) { return parseFloat(v); })
    if (num.length>3) {
        return {
            pickup:{lng:num[1],lat:num[2]},
            dropoff:{lng:num[4],lat:num[5]}
        };
    }
    return {
            lng:num[1],
            lat:num[2]
        };
}

function points2positions(str) {
    var numberPattern = /[+-]?\d+(\.\d+)?/g;
    num = str.match( numberPattern ).map(function(v) { return parseFloat(v); })
    res = [];
    for (var i=0;i<num.length;i+=3) {
        res.push({position:[num[i+2],num[i+1]]});
    }
    return res;
}

function loc2str(loc) {
    return '(' + loc.lng.toFixed(3)+','+loc.lat.toFixed(3)+')';
}

require(['moment', 'jquery', 'datatables.net-bs','bootstrap'], function(moment, $){
    $(document).ready(function() {
        tripstable = $('#trips').DataTable( {
            "processing": false,//true,
            "serverSide": false,//true,
            "paging": true,
            "order": [],
            "ajax": ajax,
            "lengthMenu": [[10, 25, 50, 100, 200, 500, 1000, 2000, 5000, 10000], [10, 25, 50,100, 200, 500, 1000, 2000, 5000, 10000]],
            "columns": [
                { "data": 'pickupTime',"render": function ( data, type, row ) {
                    return  moment(data);
                    }, 
                },
                { "data": 'pickupPoint',"class": "location","render": function ( data, type, row ) 
                    {
                        try {
                            trip = point2lnglat(data+row['dropoffPoint']);
                            res = loc2str(trip.pickup) + '->' + loc2str(trip.dropoff);
                        } catch (e) {
                            console.log(data+row['dropoffPoint'])
                            return '';
                        }
                        return res;
                    },
                },
                { "data": 'dropoffPoint','visible':false},
                { "data": 'totalAmount'},
                { "data": 'tripDistance'}
            ]
        } );
        detailRows=[];
        $('#trips tbody').on( 'click', 'tr td.location', function () {
            var tr = $(this).closest('tr');
            var row = tripstable.row( tr );
            var idx = $("#trips tbody tr").index(tr);
            singleData = point2lnglat(row.data().pickupPoint+row.data().dropoffPoint);
            single_map.draw();
        } );
        $('#trips').on( 'init.dt', function () {
            $('#map-button').css("display", "block");
        } )
    } );
});