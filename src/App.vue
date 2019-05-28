<template>
    <div id="app">
        <v-app>
            <v-card>
                <v-card-title>

                  <v-select @change="changedAction" :items="campain" v-model="e2" label="Aktion" class="mr-3"></v-select>

                    <v-autocomplete @change="changedValue" :items="ranking" :menu-props="{maxHeight:'700'}" v-model="e1" label="Rangliste" item-text="name" item-value="name" >
                        <template slot="item" slot-scope="data">
                            <template  id="scroll-target" style="max-height: 400px" class="scroll-y" v-if="typeof data.item !== 'object'">
                                <v-list-tile-content v-text="data.item"></v-list-tile-content>
                            </template>
                            <template v-else>
                                <v-list-tile-avatar :tile="true" v-if="data.item.avatar">
                                    <img :src="data.item.avatar">
                                </v-list-tile-avatar>
                                <v-list-tile-content>
                                    <v-list-tile-title v-html="data.item.name"></v-list-tile-title>
                                    <v-list-tile-sub-title v-html="data.item.group"></v-list-tile-sub-title>
                                </v-list-tile-content>
                            </template>
                        </template>
                    </v-autocomplete>

                    <v-spacer></v-spacer>

                    <v-text-field v-model="search" append-icon="search" label="Suche in Tabelle ..." single-line hide-details></v-text-field>

                </v-card-title>

                <v-progress-linear slot="progress" color="blue" indeterminate></v-progress-linear>

                <v-data-table :disable-initial-sort="true" :search="search" :headers="headers" :items="tableData" no-data-text='Keine Daten gefunden.' hide-actions item-key="artname"
                    :loading="loading" class="elevation-1">
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
                    <template slot="expand">
                    <Chart>
                    </Chart>
                    </template>
                    <v-alert slot="no-results" :value="true" color="error" icon="warning">
                        Leider wurde Dein Suchbegriff "{{ search }}" nicht gefunden.
                    </v-alert>
                     <template slot="footer" :items="footer" v-if="footer">
      <td colspan="100%">
        Anzahl Meldungen: <strong>{{footer.meldungen}}</strong><br>
        Anzahl Beobachtungen: <strong>{{footer.beobachtungen}}</strong>
      </td>
    </template>
                </v-data-table>
                </v-card>
        </v-app>
        </div>
</template>

<script>
import Chart from './components/Chart'
import * as $ from 'jquery';
import Papa from 'papaparse';

let searchParams = new URLSearchParams(window.location.search);

let campains = {
  '2018-06' : { text: 'Juni 2018', value: '2018-06'},
  '2018-08' : { text: 'August 2018', value: '2018-08'},
  '2019-06' : { text: 'Juni 2019', value: '2019-06'},
}

function loadData(vi,campain){
     $.ajax({
        type: "GET",
        url: 'https://karten.nabu.de/insektensommer/data/beobachtungen-'+campain+'.csv',
        //url: 'assets/data/beobachtungen-'+campain+'.csv',
        dataType: "text",
        success: function(data) {processData(vi,data);}
     });
}
function processData(vi,data){
        var results = Papa.parse(data, {
          header: true
        });
        vi.insects = results.data;
        var insekten = vi.insects;
        const unique = new Map();
        insekten.forEach(item => {
          const entry = unique.get(item.artname);
          if (!entry) {
            unique.set(item.artname, {
              artname: item.artname,
              taxon: item.taxon,
              gattung: item.gattung,
              anzahl: Number.parseInt(item.anzahl),
              meldungen: 1
            });
          } else {
            ++entry.meldungen;
            entry.anzahl += Number.parseInt(item.anzahl);
          }
        });
        const top = [...unique.values()];
        top.sort(function(a, b) {
          return b.meldungen - a.meldungen;
        });

        const top100 = top.slice(0, 100);
        for (let i = 0; i < top100.length; i++) {
          top100[i].rang = i + 1;
          top100[i].durchschnitt = Number.parseFloat(
            Number.parseInt(top100[i].anzahl) / Number.parseInt(top100[i].meldungen)
          ).toFixed(2);
        }
        vi.tableData = top100;
        vi.top100 = top100;
        vi.footer = {
        beobachtungen : vi.insects.length-1,
        meldungen : anzahlMeldungen(vi.insects)-1
        }
        vi.loading = false;

}

function anzahlMeldungen(insekten) {
  var beobachtungen = [];
  insekten.forEach(function(insekt) {
    beobachtungen.push([insekt.lat, insekt.lon]);
  });

  var meldungen = beobachtungen
    .map(JSON.stringify)
    .reverse()
    .filter(function(e, i, a) {
      return a.indexOf(e, i + 1) === -1;
    })
    .reverse()
    .map(JSON.parse);
  return meldungen.length;
}

function anzahlLebensraum(insekten, lebensraum) {
  let beobachtungen = insekten.filter(insekt => insekt.lebensraum === lebensraum);

  return { beobachtungen: beobachtungen.length, meldungen: anzahlMeldungen(beobachtungen) };
}

function anzahlBundesland(insekten, bundesland) {
  let beobachtungen = insekten.filter(insekt => insekt.bundesland === bundesland);

  return { beobachtungen: beobachtungen.length, meldungen: anzahlMeldungen(beobachtungen) };
}

function top5bundesland(insekten, bundesland) {
  const bl = insekten.filter(insekt => insekt.bundesland === bundesland);
  const map = new Map();
  bl.forEach(item => {
    const entry = map.get(item.artname);
    if (!entry) {
      map.set(item.artname, {
        artname: item.artname,
        taxon: item.taxon,
        gattung: item.gattung,
        anzahl: Number.parseInt(item.anzahl),
        meldungen: 1
      });
    } else {
      ++entry.meldungen;
      entry.anzahl += Number.parseInt(item.anzahl);
    }
  });
  const top = [...map.values()];
  top.sort(function(a, b) {
    return b.meldungen - a.meldungen;
  });
  let top5 = top.slice(0, 5);
  for (let i = 0; i < top5.length; i++) {
    top5[i].rang = i + 1;
    top5[i].durchschnitt = Number.parseFloat(
      Number.parseInt(top5[i].anzahl) / Number.parseInt(top5[i].meldungen)
    ).toFixed(2);
  }
  return top5;
}

function lebensraumTop5(insekten, lebensraum) {
  const l = insekten.filter(insekt => insekt.lebensraum === lebensraum);
  const map = new Map();
  l.forEach(item => {
    const entry = map.get(item.artname);
    if (!entry) {
      map.set(item.artname, {
        artname: item.artname,
        taxon: item.taxon,
        gattung: item.gattung,
        anzahl: Number.parseInt(item.anzahl),
        meldungen: 1
      });
    } else {
      ++entry.meldungen;
      entry.anzahl += Number.parseInt(item.anzahl);
    }
  });
  const top = [...map.values()];
  top.sort(function(a, b) {
    return b.meldungen - a.meldungen;
  });
  let top5 = top.slice(0, 5);
  for (let i = 0; i < top5.length; i++) {
    top5[i].rang = i + 1;
    top5[i].durchschnitt = Number.parseFloat(
      Number.parseInt(top5[i].anzahl) / Number.parseInt(top5[i].meldungen)
    ).toFixed(2);
  }
  return top5;
}

export default {
  name: 'app',
  components:{
    Chart
  },
  data () {
    return {
    search: '',
    loading: true,
    footer: {
    },
    campain: [{text: 'Juni 2019', value: '2019-06'},{text: 'August 2018', value: '2018-08'},{text: 'Juni 2018', value: '2018-06'}],
    headers: [
      { text: 'Rang', value: 'rang' },
      { text: 'Insektenart', value: 'artname' },
      { text: 'Meldungen', value: 'meldungen' },
      { text: 'Anzahl', value: 'anzahl' },
      { text: 'Individuen pro Meldung', value: 'durchschnitt' },
      { text: 'Gattung', value: 'gattung' },
      { text: 'Taxon', value: 'taxon' }
    ],
    insects: [],
    tableData: [],
    bl: [],
    top100: [],
    states: ['Niedersachsen', 'Bremen'],
    e1: {name:'Top 100'},
    e2: { text: 'Juni 2019', value: '2019-06'},
    ranking: [
      { header: 'Ranglisten' },
      { name: 'Top 100', avatar: 'images/brd.svg' },
      { divider: true },
      { header: 'TOP5 Bundesländer' },
      { name: 'Baden-Württemberg', avatar: 'images/bw.svg' },
      { name: 'Bayern', avatar: 'images/by.svg' },
      { name: 'Brandenburg & Berlin', avatar: 'images/bb_be.svg' },
      { name: 'Hessen', avatar: 'images/he.svg' },
      { name: 'Mecklenburg-Vorpommern', avatar: 'images/mv.svg' },
      { name: 'Niedersachsen & Bremen', avatar: 'images/ni_hb.svg' },
      { name: 'Nordrhein-Westfalen', avatar: 'images/nw.svg' },
      { name: 'Rheinland-Pfalz', avatar: 'images/rp.svg' },
      { name: 'Saarland', avatar: 'images/sl.svg' },
      { name: 'Sachsen', avatar: 'images/sn.svg' },
      { name: 'Sachsen-Anhalt', avatar: 'images/st.svg' },
      {
        name: 'Schleswig-Holstein & Hamburg',
        avatar: 'images/sh_hh.svg'
      },
      { name: 'Thüringen', avatar: 'images/th.svg' },
      { divider: true },
      { header: 'TOP5 Lebensraum' },
      { name: 'Garten' },
      { name: 'Balkon' },
      { name: 'Park' },
      { name: 'Wiese' },
      { name: 'Wald' },
      { name: 'Feld' },
      { name: 'Teich' },
      { name: 'Bach/Fluss' },
      { name: 'Sonstiges' }
    ]
    }
  },
  created: function() {

    let param;
    if (searchParams.has('campain')) {
      param = searchParams.get('campain');
      this.e2 = campains[param];
      } else {
        // Default
        param = '2019-06';
        this.e2=  campains[param];
      }
      loadData(this,param);

  },
  mounted: function(){
  },
  methods: {
    openTChart: function(props){
      props.expanded = !props.expanded;
    },
    changedAction: function(value){
      this.e1 = {name : 'Top 100'};
      loadData(this,value);
    },
    changedValue: function(value) {
      if (value === 'Top 100') {
        this.tableData = this.top100;
        //this.footer = {
        //  meldungen: 2760,
        //  beobachtungen: 23739
        //};
        // TODO: Fix reporting of 23740 entries(beobachtungen). Should be 23739. Because 1st must be the header. Strange
        this.footer = {
        beobachtungen : this.insects.length-1,
        meldungen : anzahlMeldungen(this.insects)-1
        }
      } else if (
        ['Garten', 'Balkon', 'Park', 'Wiese', 'Wald', 'Feld', 'Teich', 'Bach/Fluss', 'Sonstiges'].includes(value)
      ) {
        if (value === 'Garten') {
          this.tableData = lebensraumTop5(this.insects, value);
          this.footer = anzahlLebensraum(this.insects, value);
        } else {
          this.tableData = lebensraumTop5(this.insects, ' ' + value);
          this.footer = anzahlLebensraum(this.insects, ' ' + value);
        }
      } else {
        this.tableData = top5bundesland(this.insects, value);
        this.footer = anzahlBundesland(this.insects, value);
      }
    }
  }
};
</script>

<style>
#tchart {
  height: 600px;
}

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

.attribution {
  padding-top: 5px;
}
.attribution > a {
  color: white;
}
.attribution > a:hover {
  color: #c3daea;
}
</style>
