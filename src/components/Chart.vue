<template>
  <td :colspan="8">
    <div
      :id="'tchart-'+artname"
      class="tchart" />
  </td>
</template>

<script>
import tauCharts from "taucharts";
import tp from "taucharts/dist/plugins/tooltip";

import "../../node_modules/taucharts/dist/taucharts.css";
import "../../node_modules/taucharts/dist/plugins/tooltip.css";
import juni2018_top100 from "./juni2018_top100.js";
import juni2018_top5Lebensraeume from "./juni2018_top5Lebensraeume";
import juni2018_top5Bundeslaender from "./juni2018_top5Bundeslaender";
import august2018_top100 from "./august2018_top100.js";
import august2018_top5Lebensraeume from "./august2018_top5Lebensraeume";
import august2018_top5Bundeslaender from "./august2018_top5Bundeslaender";

export default {
  data: () => ({
    //august2018_top100: august2018_top100,
    juni2018_top100: juni2018_top100,
    juni2018_top5Lebensraeume: juni2018_top5Lebensraeume,
    juni2018_top5Bundeslaender: juni2018_top5Bundeslaender,
    august2018_top100: august2018_top100,
    august2018_top5Lebensraeume: august2018_top5Lebensraeume,
    august2018_top5Bundeslaender: august2018_top5Bundeslaender,
    selectedCampain: "",
    selectedRanking: "",
    actualCampain: {},
    artname: "",
    tchartData: [],
    headersLength: 0
  }),
  mounted() {
    this.selectedCampain = this.$attrs['selected-campain'];
    this.selectedRanking = this.$attrs['selected-ranking'];
    this.artname = this.$attrs.props.item.artname;
    //this.headersLength = this.$attrs.props.headers.length;

    this.createData();
    this.$nextTick(() => {
      this.createTChart();
      console.log("tick")
    });
  },
  methods: {
    createData: function() {
            if (this.selectedRanking.name == "Top 100") {
        this.tchartData = [];
        if (
          this.selectedCampain == "2019-06" ||
          this.selectedCampain == "2019-08"
        ) {
          let campain201806 = this.juni2018_top100.find(
            o => o.artname === this.artname
          );
          if (campain201806 !== undefined) {
            campain201806["aktion"] = "Juni 2018";
            this.tchartData.push(campain201806);
          }
          this.actualCampain["aktion"] = this.selectedCampain;
          this.tchartData.push(this.actualCampain);
        } else {
          let campain201808 = this.august2018_top100.find(
            o => o.artname === this.artname
          );
          if (campain201808 !== undefined) {
            campain201808["aktion"] = "August 2018";
            this.tchartData.push(campain201808);
          }
          this.actualCampain["aktion"] = this.selectedCampain;
          this.tchartData.push(this.actualCampain);
        }
        // Strange TauCharts seems to ignore duplicated entries.
        // Which is a pro, it seems no different case handling is needed.
      } else if (
        this.selectedRankingGroup !== undefined &&
        this.selectedRankingGroup == "TOP5 Lebensräume"
      ) {
        this.tchartData = [];
        if (
          this.selectedCampain == "Juni 2019" ||
          this.selectedCampain == "Juni 2018"
        ) {
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
        } else {
          let campain201808Lebensraum = this.august2018_top5Lebensraeume.find(
            o => o.name === this.selectedRanking
          );
          let campain201808 = campain201808Lebensraum.data.find(
            o => o.artname === this.artname
          );
          if (campain201808 !== undefined) {
            campain201808["aktion"] = "August 2018";
            this.tchartData.push(campain201808);
          }
          this.actualCampain["aktion"] = this.selectedCampain;
          this.tchartData.push(this.actualCampain);
        }
      } else if (
        this.selectedRankingGroup !== undefined &&
        this.selectedRankingGroup == "TOP5 Bundesländer"
      ) {
        this.tchartData = [];
        if (
          this.selectedCampain == "Juni 2019" ||
          this.selectedCampain == "Juni 2018"
        ) {
          let campain201806Bundesland = this.juni2018_top5Bundeslaender.find(
            o => o.name === this.selectedRanking
          );
          let campain201806 = campain201806Bundesland.data.find(
            o => o.artname === this.artname
          );
          if (campain201806 !== undefined) {
            campain201806["aktion"] = "Juni 2018";
            this.tchartData.push(campain201806);
          }
          this.actualCampain["aktion"] = this.selectedCampain;
          this.tchartData.push(this.actualCampain);
        } else {
          let campain201808Bundesland = this.august2018_top5Bundeslaender.find(
            o => o.name === this.selectedRanking
          );
          let campain201808 = campain201808Bundesland.data.find(
            o => o.artname === this.artname
          );
          if (campain201808 !== undefined) {
            campain201808["aktion"] = "August 2018";
            this.tchartData.push(campain201808);
          }
          this.actualCampain["aktion"] = this.selectedCampain;
          this.tchartData.push(this.actualCampain);
        }
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
