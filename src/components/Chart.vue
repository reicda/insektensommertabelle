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
//import august2018_top100 from "./august2018_top100.js";
import juni2018_top100 from "./juni2018_top100.js";
import juni2018_top5Lebensraeume from "./juni2018_top5Lebensraeume";
import juni2018_top5Bundeslaender from "./juni2018_top5Bundeslaender";

export default {
  data: () => ({
    //august2018_top100: august2018_top100,
    juni2018_top100: juni2018_top100,
    juni2018_top5Lebensraeume: juni2018_top5Lebensraeume,
    juni2018_top5Bundeslaender: juni2018_top5Bundeslaender,
    selectedCampain: "",
    selectedRanking: "",
    selectedRankingGroup: "",
    actualCampain: {},
    artname: "",
    tchartData: []
  }),
  mounted() {
    this.selectedCampain = this.$attrs.value[1].text;
    this.artname = this.$attrs.value[0].item.artname;
    this.actualCampain = this.$attrs.value[0].item;
    this.selectedRanking = this.$attrs.value[2].name;
    this.selectedRankingGroup = this.$attrs.value[2].group;

    this.createData();
    this.$nextTick(() => {
      this.createTChart();
    });
  },
  methods: {
    createData: function() {
      if (this.selectedRanking == "Top 100") {
        this.tchartData = [];
        let campain201806 = this.juni2018_top100.find(
          o => o.artname === this.artname
        );
        //let campain201808 = this.august2018_top100.find(
        //  o => o.artname === this.artname
        //);
        if (campain201806 !== undefined) {
          campain201806["aktion"] = "Juni 2018";
          this.tchartData.push(campain201806);
        }
        //if (campain201808 !== undefined) {
        //  campain201808["aktion"] = "August 2018";
        //  this.tchartData.push(campain201808);
        //}
        this.actualCampain["aktion"] = this.selectedCampain;
        this.tchartData.push(this.actualCampain);
        // Strange TauCharts seems to ignore duplicated entries.
        // Which is a pro, it seems no different case handling is needed.
      } else if (this.selectedRankingGroup !== undefined && this.selectedRankingGroup == "TOP5 Lebensräume") {
        this.tchartData = [];
        let campain201806Lebensraum = this.juni2018_top5Lebensraeume.find(
          o => o.name === this.selectedRanking
        );
        let campain201806 = campain201806Lebensraum.data.find(
          o => o.artname === this.artname
        );
        if (campain201806 !== undefined) {
          campain201806["aktion"] = "Juni 2018";
          this.tchartData.push(campain201806);
        }
        this.actualCampain["aktion"] = this.selectedCampain;
        this.tchartData.push(this.actualCampain);
      } else if (this.selectedRankingGroup !== undefined && this.selectedRankingGroup == "TOP5 Bundesländer") {
        this.tchartData = [];
        let campain201806Bundesland= this.juni2018_top5Bundeslaender.find(
          o => o.name === this.selectedRanking
        );
        let campain201806 = campain201806Bundesland.data.find(
          o => o.name === this.name
        );
        if (campain201806 !== undefined) {
          campain201806["aktion"] = "Juni 2018";
          this.tchartData.push(campain201806);
        }
        this.actualCampain["aktion"] = this.selectedCampain;
        this.tchartData.push(this.actualCampain);
      }
    },
    createTChart: function() {
      var chart = new tauCharts.Chart({
        plugins: [tp()],
        guide: {
          x: {
            label: { text: "Aktion" }
          },
          y: {
            label: { text: "Meldungen" }
          },
          showGridLines: "xy"
        },
        data: this.tchartData,
        type: "bar",
        x: "aktion",
        y: "meldungen",
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
  width: 50%;
}
</style>