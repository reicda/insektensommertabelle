<template>
  <div id="app">
    <v-app>
      <v-card>
        <v-card-title>
          <v-select
            @change="changedAction"
            :items="campains"
            v-model="selectedCampain"
            label="Aktion"
            class="mr-3"
          ></v-select>

          <v-autocomplete
            @change="changeRanking"
            :items="rankings"
            :menu-props="{maxHeight:'700'}"
            v-model="selectedRanking"
            label="Rangliste"
            item-text="name"
            item-value="name"
            :hint="`${selectedRanking.group?selectedRanking.group:''}`"
            return-object
          >
            <template slot="item" slot-scope="data">
              <template
                id="scroll-target"
                style="max-height: 400px"
                class="scroll-y"
                v-if="typeof data.item !== 'object'"
              >
                <v-list-tile-content v-text="data.item"></v-list-tile-content>
              </template>
              <template v-else>
                <v-list-tile-avatar :tile="true" v-if="data.item.avatar">
                  <img :src="data.item.avatar">
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title v-html="data.item.name"></v-list-tile-title>
                  <!--v-list-tile-sub-title v-html="data.item.group"></v-list-tile-sub-title-->
                </v-list-tile-content>
              </template>
            </template>
          </v-autocomplete>

          <v-spacer></v-spacer>

          <v-text-field
            v-model="search"
            append-icon="search"
            label="Suche in Tabelle ..."
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>

        <v-progress-linear slot="progress" color="blue" indeterminate="true"></v-progress-linear>

        <v-data-table
          :disable-initial-sort="true"
          :search="search"
          :headers="headers"
          :items="tableData"
          no-data-text="Keine Daten gefunden."
          hide-actions
          item-key="artname"
          :loading="loading"
          class="elevation-1"
          ref="dTable"
        >
          <template slot="items" slot-scope="props">
            <tr @click="openTChart(props)">
              <td>{{ props.item.rang}}</td>
              <td class="text-xs-left">{{ props.item.artname}}</td>
              <td class="text-xs-left">{{ props.item.meldungen}}</td>
              <td class="text-xs-left">{{ props.item.anzahl}}</td>
              <td class="text-xs-left">{{ props.item.durchschnitt}}</td>
              <td class="text-xs-left">{{ props.item.gattung}}</td>
              <td class="text-xs-left">{{ props.item.taxon}}</td>
            </tr>
          </template>

          <template v-slot:expand="props">
            <Chart :props="props" :value="[props,selectedCampain,selectedRanking]"></Chart>
          </template>

          <v-alert
            slot="no-results"
            :value="true"
            color="error"
            icon="warning"
          >Leider wurde Dein Suchbegriff "{{ search }}" nicht gefunden.</v-alert>

          <template slot="footer" :items="footer" v-if="footer">
            <td colspan="100%">
              Anzahl Meldungen (insgesamt):
              <strong>{{footer.meldungen}}</strong>
              <br>Anzahl Beobachtungen (ingesamt):
              <strong>{{footer.beobachtungen}}</strong>
            </td>
          </template>
        </v-data-table>
      </v-card>
    </v-app>
  </div>
</template>

<script>
import Chart from "./components/Chart";
import Papa from "papaparse";

export default {
  name: "app",
  components: {
    Chart
  },
  data() {
    return {
      search: "",
      loading: true,
      footer: {
        beobachtungen: 0,
        meldungen: 0
      },
      campains: [
        { text: "Juni 2019", value: "2019-06" },
        { text: "August 2018", value: "2018-08" },
        { text: "Juni 2018", value: "2018-06" }
      ],
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
      selectedRanking: { name: "Top 100" },
      selectedCampain: { text: "Juni 2019", value: "2019-06" },
      rankings: [
        { header: "Ranglisten" },
        { name: "Top 100", avatar: "images/brd.svg" },
        { divider: true },
        { header: "TOP5 Bundesländer" },
        {
          name: "Baden-Württemberg",
          avatar: "images/bw.svg",
          group: "TOP5 Bundesländer"
        },
        { name: "Bayern", avatar: "images/by.svg", group: "TOP5 Bundesländer" },
        {
          name: "Brandenburg & Berlin",
          avatar: "images/bb_be.svg",
          group: "TOP5 Bundesländer"
        },
        { name: "Hessen", avatar: "images/he.svg", group: "TOP5 Bundesländer" },
        {
          name: "Mecklenburg-Vorpommern",
          avatar: "images/mv.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Niedersachsen & Bremen",
          avatar: "images/ni_hb.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Nordrhein-Westfalen",
          avatar: "images/nw.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Rheinland-Pfalz",
          avatar: "images/rp.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Saarland",
          avatar: "images/sl.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Sachsen",
          avatar: "images/sn.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Sachsen-Anhalt",
          avatar: "images/st.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Schleswig-Holstein & Hamburg",
          avatar: "images/sh_hh.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Thüringen",
          avatar: "images/th.svg",
          group: "TOP5 Bundesländer"
        },
        { divider: true },
        { header: "TOP5 Lebensräume" },
        { name: "Garten", group: "TOP5 Lebensräume" },
        { name: "Balkon", group: "TOP5 Lebensräume" },
        { name: "Park", group: "TOP5 Lebensräume" },
        { name: "Wiese", group: "TOP5 Lebensräume" },
        { name: "Wald", group: "TOP5 Lebensräume" },
        { name: "Feld", group: "TOP5 Lebensräume" },
        { name: "Teich", group: "TOP5 Lebensräume" },
        { name: "Bach/Fluss", group: "TOP5 Lebensräume" },
        { name: "Sonstiges", group: "TOP5 Lebensräume" }
      ]
    };
  },
  created: function() {
    let searchParams = new URLSearchParams(window.location.search);
    let param;
    if (searchParams.has("campain")) {
      param = searchParams.get("campain");
      this.selectedCampain = this.campains.find(o => o.value == param);
    }
  },
  mounted: function() {
    this.loadData();
  },
  methods: {
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
    loadData() {
      this.tableData = [];
      this.beobachtungen = [];
      this.loading = true;
      //fetch("/data/beobachtungen-" + this.selectedCampain.value + ".csv")
      fetch(
        "https://karten.nabu.de/insektensommer/data/beobachtungen-" +
          this.selectedCampain.value +
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
      // TODO: Fix if other rankings are implemented!
      if (
        this.selectedRanking.name === "Top 100" ||
        this.selectedRanking.group === "TOP5 Lebensräume" ||
        this.selectedRanking.group === "TOP5 Bundesländer"
      ) {
        props.expanded = !props.expanded;
      }
    },
    changedAction: function(value) {
      //close all expanded slots
      for (let i = 0; i < this.tableData.length; i += 1) {
        const item = this.tableData[i];
        this.$set(this.$refs.dTable.expanded, item.artname, false);
      }
      this.tableData = [];
      this.footer.meldungen = 0;
      this.footer.beobachtungen = 0;
      this.selectedRanking = { name: "Top 100" };
      this.selectedCampain = this.campains.find(o => o.value == value);
      this.loadData();
    },
    changeRanking: function(obj) {
      this.tableData = [];
      //this.allTop5Bundeslaender();
      //this.allTop5Lebensraeume();
      if (obj.name === "Top 100") {
        this.loading = true;
        this.tableData = this.top(this.beobachtungen, 100);
        this.footer.beobachtungen = this.beobachtungen.length;
        this.footer.meldungen = this.anzahlMeldungen(this.beobachtungen);
        this.loading = false;
      } else if (obj.group === "TOP5 Lebensräume") {
        if (obj.name === "Garten") {
          let beobachtungenLebensraum = this.lebensraum(
            this.beobachtungen,
            obj.name
          );
          this.tableData = this.top(beobachtungenLebensraum, 5);
        } else {
          let beobachtungenLebensraum = this.lebensraum(
            this.beobachtungen,
            " " + obj.name
          );
          this.tableData = this.top(beobachtungenLebensraum, 5);
        }
      } else if (obj.group === "TOP5 Bundesländer") {
        let beobachtungenBundesland = this.bundesland(
          this.beobachtungen,
          obj.name
        );
        this.tableData = this.top(beobachtungenBundesland, 5);
      }
      //close all expanded slots
      for (let i = 0; i < this.tableData.length; i += 1) {
        const item = this.tableData[i];
        this.$set(this.$refs.dTable.expanded, item.artname, false);
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

.avatar img {
  border-radius: 0%;
}

.white--text.card {
  background-color: #0168b3 !important;
}

th.column:nth-child(5) {
  white-space: pre-wrap;
}
</style>
