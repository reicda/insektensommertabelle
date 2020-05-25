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
import august2018_top100 from "./august2018_top100.js";
import juni2018_top100 from "./juni2018_top100.js";

import juni2018_top100Bundeslaender from "./juni2018_top100Bundeslaender";
import august2018_top100Bundeslaender from "./august2018_top100Bundeslaender";
import juni2019_top100Bundeslaender from "./juni2019_top100Bundeslaender";
import august2019_top100Bundeslaender from "./august2019_top100Bundeslaender";

import juni2018_top5Lebensraeume from "./juni2018_top5Lebensraeume";
import august2018_top5Lebensraeume from "./august2018_top5Lebensraeume";
import juni2019_top5Lebensraeume from "./juni2019_top5Lebensraeume";
import august2019_top5Lebensraeume from "./august2019_top5Lebensraeume";

export default {
  data: () => ({
    juni2018_top100: juni2018_top100,
    august2018_top100: august2018_top100,
    selectedCampain: "",
    selectedRanking: "",
    selectedInsect: {},
    past_top100: [],
    past_top5Lebensraeume: [],
    past_top100Bundeslaender: [],
    artname: "",
    tchartData: []
  }),
  created() {
    this.past_top100.push({
      aktion: { text: "Juni 2018", value: "2018-06" },
      top100: this.juni2018_top100
    });
    this.past_top100.push({
      aktion: { text: "August 2018", value: "2018-08" },
      top100: this.august2018_top100
    });
    this.past_top100Bundeslaender.push(juni2018_top100Bundeslaender)
    this.past_top100Bundeslaender.push(august2018_top100Bundeslaender)
    this.past_top100Bundeslaender.push(juni2019_top100Bundeslaender)
    this.past_top100Bundeslaender.push(august2019_top100Bundeslaender)
    this.past_top5Lebensraeume.push(juni2018_top5Lebensraeume)
    this.past_top5Lebensraeume.push(august2018_top5Lebensraeume)
    this.past_top5Lebensraeume.push(juni2019_top5Lebensraeume)
    this.past_top5Lebensraeume.push(august2019_top5Lebensraeume)
  },
  mounted() {
    this.selectedCampain = this.$attrs["selected-campain"];
    this.selectedRanking = this.$attrs["selected-ranking"];
    this.artname = this.$attrs.props.item.artname;
    this.selectedInsect = this.$attrs.props.item;

    this.createChart();
    this.$nextTick(() => {
      this.renderTChart();
      console.log("tick");
    });
  },
  methods: {
    createChart: function() {
      this.tchartData = [];

      // prepare data for selection (selected insect) for chart
      let insect = this.selectedInsect;

      const group = this.selectedRanking.value;

      var month_index = this.selectedCampain.value.slice(-2);
      let tcd = this.tchartData;

      switch (group) {
        case "top100": {
          this.prepareData(this.past_top100, this.selectedRanking, insect, tcd, month_index);
          break;
        }
        case "top100Bundeslaender":
          this.prepareData(
            this.past_top100Bundeslaender,
            this.selectedRanking,
            insect,
            tcd,
            month_index
          );
          break;
        case "top5Lebensraeume":
          this.prepareData(
            this.past_top5Lebensraeume,
            this.selectedRanking,
            insect,
            tcd,
            month_index
          );
          break;
        default:
          console.log("default");
      }
      // Create actual insect as last
      insect.aktion = this.selectedCampain.text;
      this.tchartData.push(insect);
    },
    prepareData: function(input, ranking, insect, tcd, month_index) {

      let group = ranking.value
      let groupName = ranking.name

      let filteredItems = input.filter(
        o => o.aktion.value.slice(-2) === month_index
      );

      if (group === "top100Bundeslaender" && groupName === "Top 100"){
      filteredItems.forEach(function(o) {
        let found = o[group].find(o => o.name=== insect.name);
        found.aktion = o.aktion.text;
        tcd.push(found);

      });
      }else{
        console.log(group)
        console.log(groupName)
      filteredItems.forEach(function(o) {
        let found = o[group].find(o => o.name=== groupName);
        let found2 = found["data"].find(x=> x.artname === insect.artname)
        if (found2 !== undefined){

        found2.aktion = o.aktion.text;
        tcd.push(found2);
        }
        });

      }
    },
    renderTChart: function() {
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
  width: 100%;
}
</style>
