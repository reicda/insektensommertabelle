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
    past_top100: [],
    past_top5Lebensraeume: [],
    past_top5Bundeslaender: [],
    artname: "",
    tchartData: [],
  }),
  created() {
      this.past_top100.push({"aktion": {"text": "Juni 2018", "value": "2018-06"}, "top100": this.juni2018_top100})
      this.past_top100.push({"aktion": {"text": "August 2018", "value": "2018-08"}, "top100": this.august2018_top100})
      this.past_top100.push({"aktion": {"text": "August 2020", "value": "2020-08"}, "top100": this.august2020_top100})
      console.log(this.past_top100)

  },
  mounted() {
    this.selectedCampain = this.$attrs['selected-campain'];
    this.selectedRanking = this.$attrs['selected-ranking'];
    this.artname = this.$attrs.props.item.artname;
    this.selectedInsect = this.$attrs.props.item;

    this.createData();
    this.$nextTick(() => {
      this.createTChart();
      console.log("tick")
    });
  },
  methods: {
    createData: function() {


      this.tchartData = [];
      this.selectedInsect.aktion=this.selectedCampain.text
      this.tchartData.push(this.selectedInsect);

      const group = this.selectedRanking.group

      var month_index =  this.selectedCampain.value.slice(-2)


      console.log(month_index)

      switch (group) {
        case "Top 100": {
          console.log("Top 100")
          let comparable = this.past_top100.filter(o => o.aktion.value.slice(-2) === month_index)
          console.log(comparable)
          let insect=this.selectedInsect
          let tcd = this.tchartData
          comparable.forEach(function(o){
            console.log(o)

          let find = o.top100.find(o=>o.name === insect.name)
          console.log(find)
          find.aktion=o.aktion.text
          tcd.push(find)


          }

          )
          break
        }
        case "TOP5 Bundesländer":
          console.log("TOP5 Bundesländer")
          break
        case "TOP5 Lebensräume":
          console.log("TOP5 Lebensräume")
          break
        default:
          console.log("default")
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
