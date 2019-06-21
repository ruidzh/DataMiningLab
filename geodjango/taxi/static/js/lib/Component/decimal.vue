<template>
    <div id="decimal">
        <div class="form-group col-lg-4">
            <label class="control-label" :for="computedNameTo">{{ name }}</label>
            <div class="row">
                <div class="col-lg-5">
                    <input :id="computedNameFrom" type="number" step="0.01" class="form-control" :name="computedNameFrom" />
                </div>
                <div class="col-sm-1"> - </div>
                <div class="col-lg-5">
                    <input :id="computedNameTo" type="number" step="0.01" class="form-control" :name="computedNameTo" />
                </div>
            </div>
        </div>
    </div>
</template>
<script>
define(['Vue'], function(Vue){
    Vue.component('decimal', {
        template: template,
        props:  ['inputName','name'],
        computed: {
            computedNameFrom: function () {
                if ( this.inputName != null ) {
                    return this.inputName + '__gte'
                }
                return 'undefined';
            },
            computedNameTo: function () {
                if ( this.inputName != null ) {
                    return this.inputName + '__lte'
                }
                return 'undefined';
            }
        }
      });
  });
</script>

