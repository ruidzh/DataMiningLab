<template>
    <div id="datetimepicker">
        <div class="form-group col-lg-4">
            <label class="control-label">{{ name }} From</label>
            <div class='input-group date' :id='computedIdFrom'>
                <input type='text' class="form-control" :name="computedNameFrom" />
                <span class="input-group-addon">
                    <span class="glyphicon glyphicon-calendar"></span>
                </span>
            </div>
        </div>
        <div class="form-group col-lg-4">
            <label class="control-label">{{ name }} To</label>
            <div class='input-group date' :id='computedIdTo'>
                <input type='text' class="form-control" :name="computedNameTo" />
                <span class="input-group-addon">
                    <span class="glyphicon glyphicon-calendar"></span>
                </span>
            </div>
        </div>
    </div>
</template>
<script>
define(['Vue'], function(Vue){
    Vue.component('datetimepicker', {
        template: template,
        props:  ['inputName','name'],
        mounted: function () {
            // `this` 指向 vm 实例
            var comp = this;
            $(function () {
                $('#'+comp.computedIdTo).datetimepicker({
                    format: 'YYYY-MM-DDTHH:mm:ssZ'
                });
                $('#'+comp.computedIdFrom).datetimepicker({
                    format: 'YYYY-MM-DDTHH:mm:ssZ'
                });
            });
        },
        computed: {
            computedIdFrom: function () {
                return 'datetimepicker_' + this.computedNameFrom;
            },
            computedIdTo: function () {
                return 'datetimepicker_' + this.computedNameTo;
            },
            computedNameFrom: function () {
                if ( this.inputName != null ) {
                    return this.inputName + 'Time__gte'
                }
                return 'undefined';
            },
            computedNameTo: function () {
                if ( this.inputName != null ) {
                    return this.inputName + 'Time__lte'
                }
                return 'undefined';
            }
        }
      });
  });
</script>

