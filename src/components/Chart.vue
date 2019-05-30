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

export default {
  data: () => ({
    top100: [],
    artname: "",
    tchartData: []
  }),
  mounted() {
    fetch("data/august2018_top100.json")
      .then(response => response.json())
      .then(data => {
        this.top100 = data;
        this.createData(this.artname);
        this.createTChart("tchart-" + this.artname, this.tchartData);
      });
    // eslint-disable-next-line
    // console.log("mounted");
    // Evil trick
    this.artname = this.$attrs.props.item.artname;
  },
  methods: {
    createData: function(artname) {
      // eslint-disable-next-line
      console.log(artname);
      // eslint-disable-next-line
      console.log(this.top100);
      let obj2018 = this.top100.find(o => o.artname === artname);
      obj2018["aktion"] = "August 2018";
      // eslint-disable-next-line
      console.log(obj2018);
      let obj2019 = this.$attrs.props.item;
      obj2019["aktion"] = "Mai 2019";
      // eslint-disable-next-line
      console.log(obj2019);
      this.tchartData.push(obj2018);
      this.tchartData.push(obj2019);
    },
    createTChart: function(tchartID, tchartData) {
      // eslint-disable-next-line
      //console.log(this.value.identifier);
      //props = createTChart(props);
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
        data: tchartData,
        type: "bar",
        x: "aktion",
        y: "anzahl",
        color: "aktion"
      });
      chart.renderTo(document.getElementById(tchartID));
    }
  }
};
</script>

<style>
.tchart {
  height: 25em;
}
</style>