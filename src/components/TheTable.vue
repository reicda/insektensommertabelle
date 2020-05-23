<template>
  <v-card>
    <TheTableHeader
      ref="dTheTableHeader"
      @update:selectedCampain="changeCampain"
      @update:selectedRanking="changeRanking" />

    <v-progress-linear
      slot="progress"
      color="blue"
      indeterminate="true" />

    <v-data-table
      ref="dTable"
      :search="searchString"
      :headers="headers"
      :items="tableData"
      no-data-text="Keine Daten gefunden."
      item-key="artname"
      :loading="loading"
      class="elevation-1"
      show-expand
      :items-per-page="100"
      hide-default-footer>
      <template
        slot="items"
        slot-scope="props">
        <tr>
          <td>{{ props.item.rang }}</td>
          <td class="text-xs-left">
            {{ props.item.artname }}
          </td>
          <td class="text-xs-left">
            {{ props.item.meldungen }}
          </td>
          <td class="text-xs-left">
            {{ props.item.anzahl }}
          </td>
          <td class="text-xs-left">
            {{ props.item.durchschnitt }}
          </td>
          <td class="text-xs-left">
            {{ props.item.gattung }}
          </td>
          <td class="text-xs-left">
            {{ props.item.taxon }}
          </td>
        </tr>
      </template>

      <template
        v-slot:expanded-item="props">
        <Chart
          :props="props"
          :selected-ranking="selectedRanking"
          :selected-campain="selectedCampain" />
      </template>

      <v-alert
        slot="no-results"
        :value="true"
        color="error"
        icon="warning">
        Leider wurde Dein Suchbegriff "{{ searchString }}" nicht gefunden.
      </v-alert>

      <template
        v-if="footer"
        slot="footer"
        :items="footer">
        <td colspan="100%">
          Anzahl Meldungen (insgesamt):
          <strong>{{ footer.meldungen }}</strong>
          <br>Anzahl Beobachtungen (ingesamt):
          <strong>{{ footer.beobachtungen }}</strong>
        </td>
      </template>
    </v-data-table>
  </v-card>
</template>
<script>
import TheTableHeader from "./TheTableHeader";
import Chart from "./Chart";
import Papa from "papaparse";

export default {
  name: "TheTable",
  components: {
    TheTableHeader,
    Chart
  },
  data() {
    return {
      selectedCampain: "",
      selectedRanking: "",
      searchString: "",
      loading: true,
      footer: {
        beobachtungen: 0,
        meldungen: 0
      },
      headers: [
        { text: "Rang", value: "rang" },
        { text: "Insektenart", value: "artname" },
        { text: "Meldungen", value: "meldungen" },
        { text: "Anzahl", value: "anzahl" },
        { text: "Individuen pro Meldung", value: "durchschnitt" },
        { text: "Gattung", value: "gattung" },
        { text: "Taxon", value: "taxon" }
      ],
      top5Lebensraeume: [],
      top5Bundeslaender: [],
      beobachtungen: [],
      tableData: [],
    };
  },
    mounted() {
    // https://dev.to/rolanddoda/8-secrets-vue-developers-must-know-5la#watch-child-properties-changes-from-parent
    this.$watch(
      "$refs.dTheTableHeader.search",
      (new_value ) => {
        this.searchString=new_value
      }
    );
  },
  methods: {
    changeCampain: function(selectedCampain) {
      //close all expanded slots
      for (let i = 0; i < this.tableData.length; i += 1) {
        const item = this.tableData[i];
        this.$set(this.$refs.dTable.expanded, item.artname, false);
      }
      this.tableData = [];
      this.footer.meldungen = 0;
      this.footer.beobachtungen = 0;
      this.selectedCampain=selectedCampain.value
      this.loadData(selectedCampain.value);
    },
    changeRanking: function(selectedRanking) {
      this.selectedRanking=selectedRanking
      console.log(selectedRanking)
      this.tableData = [];
      //this.allTop5Bundeslaender();
      //this.allTop5Lebensraeume();
      if (selectedRanking.name === "Top 100") {
        this.loading = true;
        this.tableData = this.top(this.beobachtungen, 100);
        this.footer.beobachtungen = this.beobachtungen.length;
        this.footer.meldungen = this.anzahlMeldungen(this.beobachtungen);
        this.loading = false;
      } else if (selectedRanking.group === "TOP5 Lebensräume") {
        if (selectedRanking.name === "Garten") {
          let beobachtungenLebensraum = this.lebensraum(
            this.beobachtungen,
            selectedRanking.name
          );
          this.tableData = this.top(beobachtungenLebensraum, 5);
        } else {
          let beobachtungenLebensraum = this.lebensraum(
            this.beobachtungen,
            " " + selectedRanking.name
          );
          this.tableData = this.top(beobachtungenLebensraum, 5);
        }
      } else if (selectedRanking.group === "TOP5 Bundesländer") {
        let beobachtungenBundesland = this.bundesland(
          this.beobachtungen,
          selectedRanking.name
        );
        this.tableData = this.top(beobachtungenBundesland, 5);
      }
      //close all expanded slots
      for (let i = 0; i < this.tableData.length; i += 1) {
        const item = this.tableData[i];
        this.$set(this.$refs.dTable.expanded, item.artname, false);
      }
    },
    allTop5Lebensraeume() {
      let top5 = [];
      let top5lebensraeume = this.rankings.filter(
        ranking => ranking.group === "TOP5 Lebensräume"
      );
      for (var value of top5lebensraeume) {
        if (value.name === "Garten") {
          top5.push({
            name: value.name,
            data: this.top(this.lebensraum(this.beobachtungen, value.name), 5)
          });
        } else {
          top5.push({
            name: value.name,
            data: this.top(
              this.lebensraum(this.beobachtungen, " " + value.name),
              5
            )
          });
        }
      }
      this.top5Lebensraeume = top5;
    },
    allTop5Bundeslaender() {
      let top5 = [];
      let bundeslaender= this.rankings.filter(
        ranking => ranking.group === "TOP5 Bundesländer"
      );
      for (var value of bundeslaender) {
        top5.push({
          name: value.name,
          data: this.top(this.bundesland(this.beobachtungen, value.name), 5)
        });
      }
      this.top5Bundeslaender = top5;
    },
    loadData(selectedCampain) {
      this.tableData = [];
      this.beobachtungen = [];
      this.loading = true;
      //fetch("/data/beobachtungen-" + this.selectedCampain.value + ".csv")
      fetch(
        "https://karten.nabu.de/insektensommer/data/beobachtungen-" +
          selectedCampain+
          ".csv",
        {
          method: "GET",
          header: { "Cache-Control": "no-cache", Pragma: "no-cache" }
        }
      )
        .then(response => response.text())
        .then(data => {
          var results = Papa.parse(data, { header: true });
          return results.data;
        })
        .then(data => {
          this.beobachtungen = data;
          this.tableData = this.top(this.beobachtungen, 100);
          this.footer.beobachtungen = this.beobachtungen.length;
          this.footer.meldungen = this.anzahlMeldungen(this.beobachtungen);
        })
        .then(() => {
          this.loading = false;
        }) // eslint-disable-next-line
        .catch(err => console.log(err));
    },
    anzahlMeldungen(beobachtungen) {
      let latlon = [];
      beobachtungen.forEach(function(beobachtung) {
        latlon.push([beobachtung.lat, beobachtung.lon]);
      });
      // prevent duplicates
      var meldungen = latlon
        .map(JSON.stringify)
        .reverse()
        .filter(function(value, index, array) {
          return array.indexOf(value, index + 1) === -1;
        })
        .reverse()
        .map(JSON.parse);
      return meldungen.length;
    },
    top(beobachtungen, slice) {
      // Totaling anzahl and meldungen for unique artname
      const uniqueMap = new Map();
      beobachtungen.forEach(beobachtung => {
        const entry = uniqueMap.get(beobachtung.artname);
        if (!entry) {
          uniqueMap.set(beobachtung.artname, {
            artname: beobachtung.artname,
            taxon: beobachtung.taxon,
            gattung: beobachtung.gattung,
            anzahl: Number.parseInt(beobachtung.anzahl),
            meldungen: 1
          });
        } else {
          ++entry.meldungen;
          entry.anzahl += Number.parseInt(beobachtung.anzahl);
        }
      });
      // Create list
      const top = [...uniqueMap.values()];
      // Sort by meldungen and then by anzahl
      top.sort(function(a, b) {
        return b.meldungen - a.meldungen || b.anzahl - a.anzahl;
      });
      // Return a sliced with pasted rang into it.
      let sliced = top.slice(0, slice);
      for (let i = 0; i < sliced.length; i++) {
        sliced[i].rang = i + 1;
        sliced[i].durchschnitt = Number.parseFloat(
          Number.parseInt(sliced[i].anzahl) /
            Number.parseInt(sliced[i].meldungen)
        ).toFixed(2);
      }
      return sliced;
    },
    lebensraum(beobachtungen, lebensraum) {
      const beobachtungenLebensraum = beobachtungen.filter(
        beobachtung => beobachtung.lebensraum === lebensraum
      );
      this.footer.beobachtungen = beobachtungenLebensraum.length;
      this.footer.meldungen = this.anzahlMeldungen(beobachtungenLebensraum);
      return beobachtungenLebensraum;
    },
    bundesland(beobachtungen, bundesland) {
      const beobachtungenBundesland = beobachtungen.filter(
        beobachtung => beobachtung.bundesland === bundesland
      );
      this.footer.beobachtungen = beobachtungenBundesland.length;
      this.footer.meldungen = this.anzahlMeldungen(beobachtungenBundesland);
      return beobachtungenBundesland;
    },
    openTChart: function(props) {
      console.log(props)
      // TODO: Fix if other rankings are implemented!
      if (
        this.selectedRanking.name === "Top 100" ||
        this.selectedRanking.group === "TOP5 Lebensräume" ||
        this.selectedRanking.group === "TOP5 Bundesländer"
      ) {
        props.expanded = !props.expanded;
      }
    }
  }
};
</script>

<style>
.datatable thead {
  background-color: #c3daea !important;
}

th:hover {
  color: black !important;
}

tr:hover {
  background-color: #e1eef4 !important;
}

.white--text.card {
  background-color: #0168b3 !important;
}

th.column:nth-child(5) {
  white-space: pre-wrap;
}
</style>
