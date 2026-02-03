<template>
  <div class="container mx-auto p-6">
    <header class="mb-8">
      <h1 class="text-4xl font-bold text-slate-800">ANS Data Analytics</h1>
      <p class="text-slate-500">Monitoramento de Operadoras e Despesas</p>
    </header>

    <section class="bg-white p-6 rounded-xl shadow-sm mb-8 border border-slate-200">
      <div class="flex flex-col md:flex-row gap-4">
        <input 
          v-model="search" 
          type="text" 
          placeholder="Digite o CNPJ ou Razão Social..." 
          class="flex-1 p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
          @keyup.enter="carregarDados"
        />
        <button @click="carregarDados(1)" class="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition">
          Filtrar
        </button>
      </div>
    </section>

    <div class="grid grid-cols-1 xl:grid-cols-4 gap-8">
      <div class="xl:col-span-3 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table class="w-full">
          <thead class="bg-slate-50 border-b">
            <tr>
              <th class="p-4 text-left text-sm font-semibold text-slate-600">CNPJ</th>
              <th class="p-4 text-left text-sm font-semibold text-slate-600">RAZÃO SOCIAL</th>
              <th class="p-4 text-left text-sm font-semibold text-slate-600">UF</th>
              <th class="p-4 text-center text-sm font-semibold text-slate-600">AÇÕES</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="op in operadoras" :key="op.cnpj" class="hover:bg-blue-50/50 transition">
              <td class="p-4 text-sm font-mono text-slate-500">{{ op.cnpj }}</td>
              <td class="p-4 text-sm font-medium text-slate-800">{{ op.razao_social }}</td>
              <td class="p-4 text-sm text-slate-600">{{ op.uf }}</td>
              <td class="p-4 text-center">
                <button @click="irParaDetalhes(op.cnpj)" class="text-blue-600 font-semibold hover:text-blue-800">Ver Histórico</button>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="p-4 border-t flex items-center justify-between bg-slate-50">
          <p class="text-sm text-slate-500">Total: {{ metadata.total }} registros</p>
          <div class="flex gap-2">
            <button @click="mudarPagina(metadata.page - 1)" :disabled="metadata.page <= 1" class="btn-paginacao">Anterior</button>
            <button @click="mudarPagina(metadata.page + 1)" :disabled="metadata.page >= metadata.total_pages" class="btn-paginacao">Próxima</button>
          </div>
        </div>
      </div>

      <div class="xl:col-span-1 space-y-6">
        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h3 class="font-bold text-slate-800 mb-4">Top UFs (Despesas)</h3>
          <BarChart v-if="loaded" :chart-data="chartData" />
        </div>
      </div>
    </div>
    <div v-if="exibindoHistorico" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
  <div class="bg-white rounded-xl max-w-2xl w-full p-6 shadow-2xl overflow-hidden">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold text-slate-800">Histórico de Despesas: {{ operadoraSelecionada }}</h2>
      <button @click="exibindoHistorico = false" class="text-gray-500 hover:text-black text-2xl">&times;</button>
    </div>

    <div class="max-h-96 overflow-y-auto">
      <table class="w-full text-sm">
        <thead class="bg-slate-100 sticky top-0">
          <tr>
            <th class="p-2 text-left">Data/Período</th>
            <th class="p-2 text-right">Valor (R$)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in historico" :key="index" class="border-b">
            <td class="p-2">{{ item.data || 'N/A' }}</td>
            <td class="p-2 text-right font-mono">R$ {{ item.valordespesas.toLocaleString('pt-BR') }}</td>
          </tr>
          <tr v-if="historico.length === 0">
            <td colspan="2" class="p-4 text-center text-slate-500">Nenhum histórico encontrado.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import api from './services/api';

const operadoras = ref([]);
const search = ref('');
const loaded = ref(false);
const metadata = reactive({ page: 1, total_pages: 1, total: 0 });

const historico = ref([]);
const operadoraSelecionada = ref(null);
const exibindoHistorico = ref(false);

const irParaDetalhes = async (cnpj) => {
  try {
    const { data } = await api.get(`/operadoras/${cnpj}/despesas`);
    historico.value = data;
    operadoraSelecionada.value = cnpj;
    exibindoHistorico.value = true;
  } catch (error) {
    alert("Erro ao buscar histórico desta operadora.");
  }
};

const carregarDados = async (pagina = 1) => {
  try {
    const { data } = await api.get('/operadoras', {
      params: { page: pagina, limit: 10, q: search.value }
    });
    operadoras.value = data.data;
    Object.assign(metadata, data.metadata);
  } catch (error) {
    console.error("Erro na API:", error);
  }
};

const mudarPagina = (novaPagina) => {
  metadata.page = novaPagina;
  carregarDados(novaPagina);
};

onMounted(carregarDados);
</script>

<style scoped>
.btn-paginacao {
  @apply px-4 py-2 bg-white border rounded shadow-sm hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed;
}
</style>