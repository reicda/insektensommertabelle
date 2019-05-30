<template>
  <v-card class="chart-card">
    <v-layout wrap pa-1>
      <v-flex xs12>
        <div :id="'tchart-'+artname" class="tchart"></div>
      </v-flex>
    </v-layout>
  </v-card>
</template>

<script>
import tauCharts from "taucharts";
import tp from "taucharts/dist/plugins/tooltip";

import "../../node_modules/taucharts/dist/taucharts.css";
import "../../node_modules/taucharts/dist/plugins/tooltip.css";
import august2018_top100 from "./august2018_top100.js";
import juni2018_top100 from "./juni2018_top100.js";

export default {
  data: () => ({
    august2018_top100: august2018_top100,
    juni2018_top100: juni2018_top100,
    artname: "",
    tchartData: []
  }),
  mounted() {
    this.artname = this.$attrs.props.item.artname;
    this.createData();
    this.$nextTick(() => {
      this.createTChart();
    });
  },
  methods: {
    createData: function() {
      this.tchartData=[];
      let campain201806 = this.juni2018_top100.find(
        o => o.artname === this.artname
      );
      let campain201808 = this.august2018_top100.find(
        o => o.artname === this.artname
      );
      campain201806["aktion"] = "Juni 2018";
      campain201808["aktion"] = "August 2018";
      let actualCampain = this.$attrs.props.item;
      actualCampain["aktion"] = "Mai 2019";
      this.tchartData.push(campain201806);
      this.tchartData.push(campain201808);
      this.tchartData.push(actualCampain);
    },
    createTChart: function() {
      var chart = new tauCharts.Chart({
        plugins: [tp()],
        guide: {
          x: {
            label: { text: "Aktion" }
          },
          y: {
            label: { text: "Anzahl" }
          },
          showGridLines: "xy"
        },
        data: this.tchartData,
        type: "bar",
        x: "aktion",
        y: "anzahl",
        color: "aktion"
      });
      chart.renderTo(document.getElementById("tchart-" + this.artname));
    }
  }
};
</script>

<style>
.tchart {
  height: 25em;
}
</style>