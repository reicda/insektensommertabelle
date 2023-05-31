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

import juni2018_top100 from "./juni2018_top100";
import august2018_top100 from "./august2018_top100";
import juni2019_top100 from "./juni2019_top100";
import august2019_top100 from "./august2019_top100";
import juni2020_top100 from "./juni2020_top100";
import august2020_top100 from "./august2020_top100";
import juni2021_top100 from "./juni2021_top100";
import august2021_top100 from "./august2021_top100";
import juni2022_top100 from "./juni2022_top100";
import august2022_top100 from "./august2022_top100";

import juni2018_top100Bundeslaender from "./juni2018_top100Bundeslaender";
import august2018_top100Bundeslaender from "./august2018_top100Bundeslaender";
import juni2019_top100Bundeslaender from "./juni2019_top100Bundeslaender";
import august2019_top100Bundeslaender from "./august2019_top100Bundeslaender";
import juni2020_top100Bundeslaender from "./juni2020_top100Bundeslaender";
import august2020_top100Bundeslaender from "./august2020_top100Bundeslaender";
import juni2021_top100Bundeslaender from "./juni2021_top100Bundeslaender";
import august2021_top100Bundeslaender from "./august2021_top100Bundeslaender";
import juni2022_top100Bundeslaender from "./juni2022_top100Bundeslaender";
import august2022_top100Bundeslaender from "./august2022_top100Bundeslaender";

import juni2018_top5Lebensraeume from "./juni2018_top5Lebensraeume";
import august2018_top5Lebensraeume from "./august2018_top5Lebensraeume";
import juni2019_top5Lebensraeume from "./juni2019_top5Lebensraeume";
import august2019_top5Lebensraeume from "./august2019_top5Lebensraeume";
import juni2020_top5Lebensraeume from "./juni2020_top5Lebensraeume";
import august2020_top5Lebensraeume from "./august2020_top5Lebensraeume";
import juni2021_top5Lebensraeume from "./juni2021_top5Lebensraeume";
import august2021_top5Lebensraeume from "./august2021_top5Lebensraeume";
import juni2022_top5Lebensraeume from "./juni2022_top5Lebensraeume";
import august2022_top5Lebensraeume from "./august2022_top5Lebensraeume";

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
    this.past_top100.push(juni2018_top100);
    this.past_top100.push(august2018_top100);
    this.past_top100.push(juni2019_top100);
    this.past_top100.push(august2019_top100);
    this.past_top100.push(juni2020_top100);
    this.past_top100.push(august2020_top100);
    this.past_top100.push(juni2021_top100);
    this.past_top100.push(august2021_top100);
    this.past_top100.push(juni2022_top100);
    this.past_top100.push(august2022_top100);

    this.past_top100Bundeslaender.push(juni2018_top100Bundeslaender);
    this.past_top100Bundeslaender.push(august2018_top100Bundeslaender);
    this.past_top100Bundeslaender.push(juni2019_top100Bundeslaender);
    this.past_top100Bundeslaender.push(august2019_top100Bundeslaender);
    this.past_top100Bundeslaender.push(juni2020_top100Bundeslaender);
    this.past_top100Bundeslaender.push(august2020_top100Bundeslaender);
    this.past_top100Bundeslaender.push(juni2021_top100Bundeslaender);
    this.past_top100Bundeslaender.push(august2021_top100Bundeslaender);
    this.past_top100Bundeslaender.push(juni2022_top100Bundeslaender);
    this.past_top100Bundeslaender.push(august2022_top100Bundeslaender);

    this.past_top5Lebensraeume.push(juni2018_top5Lebensraeume);
    this.past_top5Lebensraeume.push(august2018_top5Lebensraeume);
    this.past_top5Lebensraeume.push(juni2019_top5Lebensraeume);
    this.past_top5Lebensraeume.push(august2019_top5Lebensraeume);
    this.past_top5Lebensraeume.push(juni2020_top5Lebensraeume);
    this.past_top5Lebensraeume.push(august2020_top5Lebensraeume);
    this.past_top5Lebensraeume.push(juni2021_top5Lebensraeume);
    this.past_top5Lebensraeume.push(august2021_top5Lebensraeume);
    this.past_top5Lebensraeume.push(juni2022_top5Lebensraeume);
    this.past_top5Lebensraeume.push(august2022_top5Lebensraeume);
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
