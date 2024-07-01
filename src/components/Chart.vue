<template>
  <td :colspan="8">
    <div
      id="tchart"
      class="tchart" />
  </td>
</template>

<script>
import tauCharts from "taucharts";
import tp from "taucharts/dist/plugins/tooltip";

import "../../node_modules/taucharts/dist/taucharts.css";
import "../../node_modules/taucharts/dist/plugins/tooltip.css";
import "./dataimport/DataImport.vue"
import ImportList from './dataimport/DataImport.vue';

export default {
  props: {
    item: { type: Object, default: () => ({}) },
    ranking: { type: Object, default: () => ({}) },
    campain: { type: Object, default: () => ({}) }
  },
  data: () => ({
    past_top100: [],
    past_top5Lebensraeume: [],
    past_top100Bundeslaender: []
  }),
  watch: {
    item: function(newVal) {
      document.getElementById("tchart").innerHTML = "";
      this.createChart(newVal);
    }
  },
  created() {
    this.past_top100 = ImportList.top100;
    this.past_top100Bundeslaender = ImportList.top100Bundeslaender;
    this.past_top5Lebensraeume = ImportList.top5Lebensraeume;
  },
  mounted() {
    document.getElementById("tchart").innerHTML = "";
    this.createChart(this.item);
    //this.$nextTick(() => {
    //  this.renderTChart();
    //  console.log("tick");
    //});
  },
  methods: {
    createChart: function(insect) {
      const group = this.ranking.value;

      var month_index = this.campain.value.slice(-2);
      const tcd = [];

      switch (group) {
        case "top100": {
          this.prepareData(this.past_top100, this.ranking, insect, tcd, month_index);
          break;
        }
        case "top100Bundeslaender":
          this.prepareData(
            this.past_top100Bundeslaender,
            this.ranking,
            insect,
            tcd,
            month_index
          );
          break;
        case "top5Lebensraeume":
          this.prepareData(
            this.past_top5Lebensraeume,
            this.ranking,
            insect,
            tcd,
            month_index
          );
          break;
        default:
          // eslint-disable-next-line
          console.log("default");
      }
       // Create actual insect as last
      insect.aktion = this.campain.text;
      tcd.push(insect);
      this.renderTChart(tcd);
    },
    prepareData: function(input, ranking, insect, tcd, month_index) {
      let group = ranking.value;
      let groupName = ranking.name;

      let filteredItems = input.filter(
        o => o.aktion.value.slice(-2) === month_index
      );

      if (group === "top100" && groupName === "Top 100") {
        filteredItems.forEach(function(o) {
          let found = o[group].find(o => o.artname === insect.artname);
          if (found !== undefined) {
            found.aktion = o.aktion.text;
            tcd.push(found);
          }
        });
      } else {
        filteredItems.forEach(function(o) {
          let found = o[group].find(o => o.name === groupName);
          let found2 = found["data"].find(x => x.artname === insect.artname);
          if (found2 !== undefined) {
            found2.aktion = o.aktion.text;
            tcd.push(found2);
          }
        });
      }
    },
    renderTChart: function(tcd) {
      new tauCharts.Chart({
        plugins: [tp()],
        guide: {
          x: {
            label: { text: "aktion" }
          },
          y: {
            label: { text: "beobachtungen" }
          },
          showGridLines: "xy"
        },
        data: tcd,
        type: "bar",
        x: "aktion",
        y: "beobachtungen",
        color: "aktion"
      }).renderTo(document.getElementById("tchart"));
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
