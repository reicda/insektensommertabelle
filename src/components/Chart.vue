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
import august2020_top100 from "./august2020_top100.js";

export default {
  data: () => ({
    juni2018_top100: juni2018_top100,
    juni2018_top5Lebensraeume: juni2018_top5Lebensraeume,
    juni2018_top5Bundeslaender: juni2018_top5Bundeslaender,
    august2018_top100: august2018_top100,
    august2020_top100: august2020_top100,
    august2018_top5Lebensraeume: august2018_top5Lebensraeume,
    august2018_top5Bundeslaender: august2018_top5Bundeslaender,
    selectedCampain: "",
    selectedRanking: "",
    selectedInsect: {},
    past_top100: [],
    past_top5Lebensraeume: [],
    past_top5Bundeslaender: [],
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
    this.past_top100.push({
      aktion: { text: "August 2020", value: "2020-08" },
      top100: this.august2020_top100
    });
    console.log(this.past_top100);
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
      insect.aktion = this.selectedCampain.text;
      this.tchartData.push(insect);

      const group = this.selectedRanking.value;
      console.log(group);

      var month_index = this.selectedCampain.value.slice(-2);
      let tcd = this.tchartData;

      switch (group) {
        case "top100": {
          this.prepareData(this.past_top100, group, insect, tcd, month_index);
          break;
        }
        case "top5Bundeslaender":
          this.prepareData(
            this.past_top5_bundeslaender,
            group,
            insect,
            tcd,
            month_index
          );
          break;
        case "top5Lebensraeume":
          this.prepareData(
            this.past_top5_lebensraeume,
            group,
            insect,
            tcd,
            month_index
          );
          break;
        default:
          console.log("default");
      }
    },
    prepareData: function(input, group, insect, tcd, month_index) {
      console.log(group);
      let filteredItems = input.filter(
        o => o.aktion.value.slice(-2) === month_index
      );
      filteredItems.forEach(function(o) {
        let found = o[group].find(o => o.name === insect.name);
        found.aktion = o.aktion.text;
        tcd.push(found);
      });
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
