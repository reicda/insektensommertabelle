<template>
  <v-card>
    <TheTableHeader
      ref="dTheTableHeader"
      @update:selectedCampain="changeCampain"
      @update:selectedRanking="changeRanking" />
    <template
      v-if="footer"
      :items="footer">
      <div id="anzahl">
        Anzahl Meldungen (insgesamt):
        <strong>{{ footer.meldungen }}</strong>
        <br>Anzahl Beobachtungen (ingesamt):
        <strong>{{ footer.beobachtungen }}</strong>
      </div>
    </template>

    <v-progress-linear
      slot="progress"
      color="blue"
      indeterminate="true" />

    <v-data-table
      ref="dTable"
      :search="searchString"
      :headers="headers"
      :items="tableData"
      :expanded="expanded"
      no-data-text="Keine Daten gefunden."
      item-key="artname"
      :loading="loading"
      class="elevation-1"
      :items-per-page="100"
      hide-default-footer
      @click:row="openTChart">
      <template #item.full_name="{ item }">
        {{ item.gattung }} {{ item.taxon }}
      </template>
      <template v-slot:expanded-item="{ item }">
        <Chart
          :item="item"
          :ranking="selectedRanking"
          :campain="selectedCampain" />
      </template>

      <v-alert
        slot="no-results"
        :value="true"
        color="error"
        icon="warning">
        Leider wurde Dein Suchbegriff "{{ searchString }}" nicht gefunden.
      </v-alert>
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
      expanded: [],
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
        { text: "Wissenschaftlicher Name", value: "full_name" }
      ],
      topAllLebensraeume: [],
      topAllBundeslaender: [],
      beobachtungen: [],
      tableData: []
    };
  },
  mounted() {
    // https://dev.to/rolanddoda/8-secrets-vue-developers-must-know-5la#watch-child-properties-changes-from-parent
    this.$watch("$refs.dTheTableHeader.search", new_value => {
      this.searchString = new_value;
    });
  },
  methods: {
    changeCampain: function(selectedCampain) {
      //close all expanded slots
      //close all expanded slots
      if (this.$refs.dTable !== undefined){
      this.$refs.dTable.expansion=false;
      }
      this.tableData = [];
      this.footer.meldungen = 0;
      this.footer.beobachtungen = 0;
      this.selectedCampain = selectedCampain;
      this.loadData(selectedCampain.value);
    },
    changeRanking: function(selectedRanking) {
      this.selectedRanking = selectedRanking;

      //close all expanded slots
      if (this.$refs.dTable !== undefined){
      this.$refs.dTable.expansion=false;
      }

      this.tableData = [];
      this.footer.beobachtungen = 0;
      this.footer.meldungen = 0;

      let group = selectedRanking.group;

      switch (group) {
        case "TOP5 Lebensräume": {
          if (selectedRanking.name === "Garten") {
            let beobachtungenLebensraum = this.lebensraum(
              this.beobachtungen,
              selectedRanking.name
            );
            this.footer.beobachtungen = beobachtungenLebensraum.length;
            this.footer.meldungen = this.anzahlMeldungen(
              beobachtungenLebensraum
            );
            this.tableData = this.top(beobachtungenLebensraum, 5);
          } else {
            // Attention! In the original data a space is prefixed.
            // Except for "Garten".
            let beobachtungenLebensraum = this.lebensraum(
              this.beobachtungen,
              " " + selectedRanking.name
            );
            this.footer.beobachtungen = beobachtungenLebensraum.length;
            this.footer.meldungen = this.anzahlMeldungen(
              beobachtungenLebensraum
            );
            this.tableData = this.top(beobachtungenLebensraum, 5);
          }
          break;
        }
        case "TOP100 Bundesländer": {
          let beobachtungenBundesland = this.bundesland(
            this.beobachtungen,
            selectedRanking.name
          );
          this.footer.beobachtungen = beobachtungenBundesland.length;
          this.footer.meldungen = this.anzahlMeldungen(beobachtungenBundesland);
          this.tableData = this.top(beobachtungenBundesland, 100);
          break;
        }
        default: {
          this.tableData = this.top(this.beobachtungen, 100);
          this.footer.beobachtungen = this.beobachtungen.length;
          this.footer.meldungen = this.anzahlMeldungen(this.beobachtungen);
        }
      }
    },
    allTopLebensraeume(number) {
      let top = [];
      let lebensraeume = this.rankings.filter(
        ranking => ranking.group === "TOP5 Lebensräume"
      );
      for (var value of lebensraeume) {
        if (value.name === "Garten") {
          top.push({
            name: value.name,
            data: this.top(this.lebensraum(this.beobachtungen, value.name), number)
          });
        } else {
          top.push({
            name: value.name,
            data: this.top(
              this.lebensraum(this.beobachtungen, " " + value.name),
              number
            )
          });
        }
      }
      this.topAllLebensraeume = { aktion: this.selectedCampain, top5Lebensraeume: top};
    },
    allTopBundeslaender(nummer) {
      let top = [];
      let bundeslaender = this.rankings.filter(
        ranking => ranking.group === "TOP100 Bundesländer"
      );
      for (var value of bundeslaender) {
        top.push({
          name: value.name,
          data: this.top(this.bundesland(this.beobachtungen, value.name), nummer)
        });
      }
      this.topAllBundeslaender = { aktion: this.selectedCampain, top100Bundeslaender: top};
    },
    loadData(selectedCampain) {
      this.tableData = [];
      this.beobachtungen = [];
      this.loading = true;
      //fetch("/data/beobachtungen-" + this.selectedCampain.value + ".csv")
      fetch(
        "https://karten.nabu.de/insektensommer/data/beobachtungen-" +
          selectedCampain +
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
        latlon.push(beobachtung.kopfid);
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
    // helper function
    allTop(){
    this.allTop100={
      aktion: this.selectedCampain,
      top100: this.tableData
    };

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
      return beobachtungenLebensraum;
    },
    bundesland(beobachtungen, bundesland) {
      const beobachtungenBundesland = beobachtungen.filter(
        beobachtung => beobachtung.bundesland === bundesland
      );
      return beobachtungenBundesland;
    },
    openTChart: function(item) {
      this.expanded = item === this.expanded[0] ? [] : [item]
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

#anzahl{
  padding-left: 16px;
  padding-bottom: 16px;

}
</style>
