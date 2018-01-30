// Declare this variable before loading RequireJS JavaScript library
// To config RequireJS after it’s loaded, pass the below object into require.config();
google_map_api_url = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyBR7Z6npapsj4l93EOv6awYTALsvvr-EZs&';
google_map_api = 'async!' + google_map_api_url;
var strFullPath = window.document.location.href;
var strPath = window.document.location.pathname;
var pos = strFullPath.indexOf(strPath);
var prePath = strFullPath.substring(0, pos);

requirejs.config({
    baseUrl: "./static/js/lib",
    shim : {
        "bootstrap" : { "deps" :['jquery'] },
        "datetimepicker" : { "deps" :['jquery','bootstrap','moment'] },
        "gmap3" : { "deps" :['jquery'] },
        "datatables" : { "deps" :['jquery','moment','bootstrap'] }
    },
    paths: {
        "jquery" : "jquery-3.2.1.min",
        "bootstrap" :  "bootstrap.min",
        "datetimepicker" : "bootstrap-datetimepicker.min",
        "moment" : "moment.min",
        "gmap3" : "gmap3.min",
        'noext' : "require_noext",
        'async': 'require_async',
        'Vue' : 'vue',
        'vue': "requirejs-vue",
        //DataTables core
        'datatables' : 'DataTables/datatables.min',
        'datatables.net' : 'DataTables/DataTables-1.10.16/js/jquery.dataTables.min',
        'datatables.net-bs' : 'DataTables/DataTables-1.10.16/js/dataTables.bootstrap.min',

        //Dependencies
        'datatables.net-autofill' : 'DataTables/AutoFill-2.2.2/js/dataTables.autoFill.min',
        'datatables.net-buttons' : 'DataTables/Buttons-1.5.0/js/dataTables.buttons.min',

        //Extra modules
        'datatables.net-buttons-bs' : 'DataTables/Buttons-1.5.0/js/buttons.bootstrap.min',
        'datatables.net-colreorder' : "DataTables/ColReorder-1.4.1/js/dataTables.colReorder.min",
        'datatables.net-rowreorder' : "DataTables/RowReorder-1.2.3/js/dataTables.rowReorder.min",
        'datatables.net-scroller' : "DataTables/Scroller-1.4.3/js/dataTables.scroller.min",
        'datatables.net-select' : "DataTables/Select-1.2.4/js/dataTables.select.min",
    }
});