<template>
  <v-card class="chart-card">
    <v-layout wrap pa-1>
      <v-flex xs12>
        <div :id="'tchart-'+count"></div>
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
    count:0,
    tchartData: [
      {
        aktion: "Mai 2018",
        artname: "Ackerhummel",
        taxon: "pascuorum",
        gattung: "Bombus",
        anzahl: 1515,
        meldungen: 293,
        rang: 1,
        durchschnitt: "5.17"
      },
      {
        aktion: "Juni 2018",
        artname: "Kleiner Kohlweißling",
        taxon: "rapae",
        gattung: "Pieris",
        anzahl: 622,
        meldungen: 225,
        rang: 2,
        durchschnitt: "2.76"
      },
      {
        aktion: "Mai 2019",
        artname: "Westliche Honigbiene",
        taxon: "mellifera",
        gattung: "Apis",
        anzahl: 2062,
        meldungen: 173,
        rang: 3,
        durchschnitt: "11.92"
      },
      {
        aktion: "Juni 2019",
        artname: "Gemeine Wespe",
        taxon: "vulgaris",
        gattung: "Vespula",
        anzahl: 1020,
        meldungen: 141,
        rang: 4,
        durchschnitt: "7.23"
      },
      {
        aktion: "Mai 2020",
        artname: "Großer Kohlweißling",
        taxon: "brassicae",
        gattung: "Pieris",
        anzahl: 414,
        meldungen: 128,
        rang: 5,
        durchschnitt: "3.23"
      }
    ]
  }),
  mounted() {
    // eslint-disable-next-line
    // console.log("mounted");
    this.createTChart("tchart-"+this.count, this.tchartData);
  },
  methods: {
    createTChart: function(tchartID, tchartData) {
      // eslint-disable-next-line
      //console.log(this.value.identifier);
      //props = createTChart(props);
      var chart = new tauCharts.Chart({
        plugins: [tp()],
        guide: {
          x: {
            label: { text: "Aktionen" }
          },
          y: {
            label: { text: "Meldungen" }
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
      this.count++;
    }
  }
};
</script>

<style>
</style>