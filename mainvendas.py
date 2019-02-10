# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWebEngineWidgets import QWebEngineView
from Views.mainVendas import Ui_ct_MainVendas
from Views.formVendas import Ui_ct_FormVenda
from functools import partial
from Crud.CrudPedidos import CrudPedidos
from Crud.CrudProdutos import CrudProdutos
from Crud.CrudClientes import CrudClientes
from Crud.CrudAReceber import CrudAReceber
from Funcoes.data import DataAtual
# from Funcoes.BuscaProdutos import BuscaProdutos


class MainVendas(Ui_ct_MainVendas, Ui_ct_FormVenda, DataAtual):

    def mainvendas(self, frame):
        super(MainVendas, self).setMainVendas(frame)
        self.frameMainVendas.show()

        """ Definindo funcões widgets"""
        # Botao Adicionar Venda
        self.bt_AddNovoVenda.clicked.connect(self.FormVendas)

        # Busca Vendas
        self.bt_BuscaVendas.clicked.connect(self.DataTabVendas)

        # Setando data Inicio e Fim da Consulta
        self.dt_InicioVenda.setDate(self.primeiroDiaMes())
        self.dt_FimVenda.setDate(self.ultimoDiaMes())

        # Tamanho das Colunas Tabela Vendas
        self.tb_Vendas.blockSignals(True)
        self.tb_Vendas.setColumnHidden(0, True)

        self.tb_Vendas.resizeRowsToContents()
        self.tb_Vendas.setColumnWidth(1, 10)
        self.tb_Vendas.setColumnWidth(2, 384)
        self.tb_Vendas.setColumnWidth(3, 160)
        self.tb_Vendas.setColumnWidth(4, 160)
        self.tb_Vendas.setColumnWidth(5, 160)
        self.tb_Vendas.setColumnWidth(6, 20)

        # Icones dos Botoes
        self.IconeBotaoForm(self.bt_AddNovoVenda,
                            self.resourcepath('Images/addVenda.svg'))
        self.IconeBotaoMenu(self.bt_BuscaVendas,
                            self.resourcepath('Images/search.png'))
        self.IconeBotaoMenu(self.bt_PrintRelatVendas,
                            self.resourcepath('Images/gtk-print.png'))

        self.DataTabVendas()

    # Populando tabela vendas
    def DataTabVendas(self):
        cliente = self.tx_BuscaVendas.text()
        busca = CrudPedidos()
        busca.dataEmissao = QtCore.QDate.toString(
            self.dt_InicioVenda.date(), "yyyy-MM-dd")

        busca.dataFim = QtCore.QDate.toString(
            self.dt_FimVenda.date(), 'yyyy-MM-dd')
        busca.ListaVendatabela(cliente)

        while self.tb_Vendas.rowCount() > 0:
            self.tb_Vendas.removeRow(0)
            pass

        i = 0
        while i < len(busca.nomeCliente):
            self.tb_Vendas.insertRow(i)
            self.conteudoTabela(self.tb_Vendas, i, 0, str(busca.idPedido[i]))

            self.TabelaStatus(self.tb_Vendas, i, 1,
                              self.StatusEntrega(busca.idStatusEntrega[i],
                                                 busca.idStatusPagamento[i]))

            self.TabelaNomeTelefone(
                self.tb_Vendas, i, 2, busca.nomeCliente[i],
                busca.telefoneCliente[i])
            self.TabelaEntrega(self.tb_Vendas, i, 3,
                               busca.dataEmissao[i],
                               self.StatusEntrega(busca.idStatusEntrega[i]), "")
            self.TabelaEntrega(self.tb_Vendas, i, 4,
                               busca.prazoEntrega[i],
                               self.StatusEntrega(busca.idStatusEntrega[i]),
                               busca.statusEntrega[i].upper())
            self.TabelaPagamento(self.tb_Vendas, i, 5,
                                 busca.valorTotal[i],
                                 self.StatusEntrega(
                                     busca.idStatusPagamento[i]),
                                 busca.statusPagamento[i].upper())

            self.botaoTabela(self.tb_Vendas, i, 6,
                             partial(self.SelectVendaId, busca.idPedido[i]), "#069")

            i += 1

    def FormVendas(self):
        self.DesativaBotaoVendas()
        self.LimpaFrame(self.ct_containerVendas)
        super(MainVendas, self).setFormVenda(self.ct_containerVendas)
        self.fr_FormVenda.show()

        # Setando Datas
        self.dt_EmissaoPedido.setDate(QtCore.QDate.currentDate())
        self.dt_PrazoEntrega.setDate(QtCore.QDate.currentDate().addDays(2))
        self.dt_EntregaPedido.setDate(QtCore.QDate.currentDate())
        self.dt_VencimentoVenda.setDate(QtCore.QDate.currentDate())

        # Icone Botoes
        self.IconeBotaoMenu(self.bt_SalvarVenda,
                            self.resourcepath('Images/salvar.png'))

        self.IconeBotaoMenu(self.bt_CancelarVenda,
                            self.resourcepath('Images/cancelar.png'))

        self.IconeBotaoMenu(
            self.bt_Entregar, self.resourcepath('Images/ico_entrega.png'))

        self.IconeBotaoMenu(
            self.bt_ImprimirVenda, self.resourcepath('Images/gtk-print.png'))

        self.IconeBotaoMenu(self.bt_GerarParcelaVenda,
                            self.resourcepath('Images/ico_conta.png'))

        self.IconeBotaoForm(self.bt_IncluirItemPedido,
                            self.resourcepath('Images/addPedido.svg'))

        # Setando Foco no Cliente id TX
        self.tx_CodClienteVenda.setFocus()

        # Checando se existe ID válido
        self.IdCheckPedido()

        # Tamanho das Colunas Tabela Itens
        self.tb_Itens.blockSignals(True)
        self.tb_Itens.setColumnHidden(0, True)
        self.tb_Itens.setColumnHidden(7, True)
        self.tb_Itens.resizeRowsToContents()
        self.tb_Itens.setColumnWidth(1, 165)
        self.tb_Itens.setColumnWidth(2, 150)
        self.tb_Itens.setColumnWidth(3, 75)
        self.tb_Itens.setColumnWidth(4, 75)
        self.tb_Itens.setColumnWidth(5, 75)
        self.tb_Itens.setColumnWidth(6, 45)

        # Tamanho tabela parcelas
        self.tb_parcelasVenda.blockSignals(True)
        self.tb_parcelasVenda.setColumnHidden(0, True)
        self.tb_parcelasVenda.setColumnWidth(1, 90)
        self.tb_parcelasVenda.setColumnWidth(2, 60)
        self.tb_parcelasVenda.setColumnWidth(3, 80)
        self.tb_parcelasVenda.setColumnWidth(4, 90)

        """ Definindo funcões widgets"""
        # Return Press Busca Id Produto
        self.tx_IdBuscaItem.returnPressed.connect(self.BuscaProdutoId)

        # Campo Busca por nome e Autocompletar Produto
        self.completer = QtWidgets.QCompleter(self)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.model = QtCore.QStringListModel(self)
        self.completer.setModel(self.model)
        self.tx_BuscaItem.setCompleter(self.completer)
        self.tx_BuscaItem.textEdited.connect(self.autocomplete)
        self.tx_BuscaItem.returnPressed.connect(self.BuscaProdutoNome)

        # Return Press Busca Id Cliente
        self.tx_CodClienteVenda.returnPressed.connect(self.BuscaClienteId)

        # Campo Busca por nome e Autocompletar Cliente
        self.tx_ClienteVenda.setCompleter(self.completer)
        self.tx_ClienteVenda.textEdited.connect(self.autocompleCliente)
        self.tx_ClienteVenda.returnPressed.connect(self.BuscaClienteNome)

        # Setando Validadot Int nos campos
        validaInt = QtGui.QIntValidator(0, 9999)
        self.tx_QntdItem.setValidator(validaInt)
        self.tx_IdBuscaItem.setValidator(validaInt)
        self.tx_CodClienteVenda.setValidator(validaInt)
        # Setando Validador float nos campos
        validarValor = QtGui.QDoubleValidator(0.00, 9999.00, 2)
        validarValor.setNotation(QtGui.QDoubleValidator.StandardNotation)
        validarValor.setDecimals(2)
        self.tx_Desconto.setValidator(validarValor)
        self.tx_Frete.setValidator(validarValor)
        # self.tx_ValorPago.setValidator(validarValor)

        # Calculo total produto por qtde item
        self.tx_QntdItem.returnPressed.connect(self.TotalItem)

        # calculando com desconto
        self.tx_Desconto.returnPressed.connect(self.TotalFinal)
        self.tx_Desconto.returnPressed.connect(self.tx_Frete.setFocus)
        self.tx_Desconto.returnPressed.connect(self.tx_Frete.selectAll)

        # calculando com frete
        self.tx_Frete.returnPressed.connect(self.TotalFinal)
        # self.tx_Frete.returnPressed.connect(self.tx_ValorPago.setFocus)
        # self.tx_Frete.returnPressed.connect(self.tx_ValorPago.selectAll)

        # Calculo Valor Pendente
        # self.tx_ValorPago.returnPressed.connect(self.TotalFinal)

        # Validar valor Recebido
        # self.tx_ValorPago.textEdited.connect(self.validarRecebimento)

        # Receber
        self.bt_GerarParcelaVenda.clicked.connect(self.gerarParcela)

        # Entregar
        self.bt_Entregar.clicked.connect(self.Entregar)

        # Add Item Tabela
        self.tx_ObsItemPedido.returnPressed.connect(self.ValidaFormAdd)
        self.bt_IncluirItemPedido.clicked.connect(self.ValidaFormAdd)

        # Botao Salvar
        self.bt_SalvarVenda.clicked.connect(self.CadVenda)
        # Botao Cancelar
        self.bt_CancelarVenda.clicked.connect(self.janelaVendas)

        # Botao Imprimir
        self.bt_ImprimirVenda.clicked.connect(self.imprimirVenda)

    # checando campo Id se é Edicao ou Nova Venda
    def IdCheckPedido(self):
        if not self.tx_CodPedido.text():
            busca = CrudPedidos()
            self.tx_CodPedido.setText(str(busca.lastIdPedido()))
            # setando dataAtual campo entrega e emissão

    # Autocomplete Produtos
    def autocomplete(self):
        produto = self.tx_BuscaItem.text()
        busca = CrudProdutos()
        busca.ListaProdutoTabela(produto)
        lista = busca.descricaoProduto
        if produto:
            self.model.setStringList(lista)

    # Busca Produto por nome
    def BuscaProdutoNome(self):
        produto = self.tx_BuscaItem.text()
        busca = CrudProdutos()
        busca.ListaProdutoTabela(produto)
        self.tx_IdBuscaItem.setText(str(busca.idProduto[0]))
        self.BuscaProdutoId()

    # Busca produtos por ID
    def BuscaProdutoId(self):
        id = int(self.tx_IdBuscaItem.text())
        busca = CrudProdutos()
        busca.SelectProdutoId(id)
        if busca.descricaoProduto:
            self.tx_BuscaItem.setText(busca.descricaoProduto)
            self.tx_ValorUnitarioItem.setText(busca.valorUnitario)
            self.tx_QntdItem.setFocus()
        else:
            self.tx_BuscaItem.setText("Produto não encontrado")
            self.tx_IdBuscaItem.clear()
            self.tx_IdBuscaItem.setFocus()

    # AutoComplete Cliente
    def autocompleCliente(self):
        cliente = self.tx_ClienteVenda.text()
        busca = CrudClientes()
        busca.ListaClientesTabela(cliente)
        lista = busca.nomeCliente
        if cliente:
            self.model.setStringList(lista)

    # Busca cliente por nome
    def BuscaClienteNome(self):
        cliente = self.tx_ClienteVenda.text()
        busca = CrudClientes()
        busca.ListaClientesTabela(cliente)
        self.tx_CodClienteVenda.setText(str(busca.idCliente[0]))
        self.BuscaClienteId()

    # Busca cliente por ID
    def BuscaClienteId(self):
        id = int(self.tx_CodClienteVenda.text())
        busca = CrudClientes()
        busca.SelectClienteID(id)
        if busca.nomeCliente:
            self.tx_ClienteVenda.setText(busca.nomeCliente)
            self.tx_TelefoneClienteVenda.setText(busca.celularCliente)
            self.tx_IdBuscaItem.setFocus()
        else:
            self.tx_ClienteVenda.setText(
                "Cliente não encontrado")
            self.tx_CodClienteVenda.clear()
            self.tx_CodClienteVenda.setFocus()

    # Calculo ValorTotalItem
    def TotalItem(self):
        id = self.tx_IdBuscaItem.text()
        busca = CrudProdutos()
        busca.SelectProdutoId(id)
        if self.tx_QntdItem.text() and self.tx_ValorUnitarioItem.text():
            if float(self.tx_QntdItem.text()) >= int(busca.qtdeAtacado):
                self.tx_ValorUnitarioItem.setText(busca.valorAtacado)
            else:
                self.tx_ValorUnitarioItem.setText(busca.valorUnitario)
            TotalItem = float(self.tx_QntdItem.text()) * \
                float(self.tx_ValorUnitarioItem.text())
            self.tx_ValorTotalItem.setText(format(TotalItem, ".2f"))
            self.bt_IncluirItemPedido.setEnabled(True)
            self.tx_ObsItemPedido.setFocus()

    def TotalFinal(self):
        total = 0

        if not int(self.tb_Itens.rowCount()) == 0 and self.tb_Itens.item(0, 5).text():
            for row in range(self.tb_Itens.rowCount()):
                total = float(self.tb_Itens.item(row, 5).text()) + total
        self.lb_SubTotalVenda.setText(format(total, ".2f"))
        self.tx_TotalFinal.setText(format(total, ".2f"))
        self.lb_ValorPendente.setText(format(total, ".2f"))

        if self.tx_Desconto.text():
            desconto = self.tx_Desconto.text().replace(',', '.')
            TotalFinal = float(total) - float(desconto)
            self.tx_TotalFinal.setText(format(TotalFinal, ".2f"))
            self.tx_Desconto.setText(
                format(float(desconto), ".2f"))
            self.lb_ValorPendente.setText(format(TotalFinal, ".2f"))

        if self.tx_Frete.text():
            frete = self.tx_Frete.text().replace(',', '.')
            TotalFinal = float(
                total) - float(self.tx_Desconto.text()) + float(frete)
            self.tx_Frete.setText(format(float(frete), ".2f"))
            self.tx_TotalFinal.setText(format(TotalFinal, ".2f"))
            self.lb_ValorPendente.setText(format(TotalFinal, ".2f"))

        if self.tx_valorRecebido.text():
            recebido = self.tx_valorRecebido.text().replace(",", ".")
            TotalFinal = float(self.tx_TotalFinal.text()) - \
                float(recebido)
            self.tx_valorRecebido.setText(
                format(float(recebido), ".2f"))
            self.lb_ValorPendente.setText(format(TotalFinal, ".2f"))

    def ValidaFormAdd(self):
        if not self.tx_CodClienteVenda.text():
            self.tx_CodClienteVenda.setFocus()
        elif not self.tx_IdBuscaItem.text():
            self.tx_IdBuscaItem.setFocus()
        elif not self.tx_BuscaItem.text():
            self.tx_BuscaItem.setFocus()
        elif not self.tx_QntdItem.text():
            self.tx_QntdItem.setFocus()
        elif not self.tx_ClienteVenda.text():
            self.tx_ClienteVenda.setFocus()
        else:
            self.AddItemTabela()

    # Adiciona Item a tabela
    def AddItemTabela(self):
        row = self.tb_Itens.rowCount()
        self.tb_Itens.insertRow(row)
        self.conteudoTabela(self.tb_Itens, row, 0,
                            self.tx_IdBuscaItem.text())
        self.conteudoTabelaLeft(self.tb_Itens, row, 1,
                                self.tx_BuscaItem.text())
        self.conteudoTabelaLeft(self.tb_Itens, row, 2,
                                self.tx_ObsItemPedido.text())

        self.conteudoTabela(self.tb_Itens, row, 3,
                            self.tx_QntdItem.text())
        self.conteudoTabela(self.tb_Itens, row, 4,
                            self.tx_ValorUnitarioItem.text())
        self.conteudoTabela(self.tb_Itens, row, 5,
                            self.tx_ValorTotalItem.text())
        self.botaoRemoveItem(self.tb_Itens, row, 6,
                             partial(self.RemoveLInha, row), "#005099")

        self.conteudoTabela(self.tb_Itens, row, 7, str(
            QtCore.QDateTime.toMSecsSinceEpoch(QtCore.QDateTime.currentDateTime())))

        self.TotalFinal()
        self.LimpaCampoAddProduto()
        self.bt_GerarParcelaVenda.setEnabled(True)

    # Removendo item da tabela e banco de dados se ouver
    def RemoveLInha(self, linha):
        REMOVE = CrudPedidos()
        REMOVE.idItemTabela = self.tb_Itens.item(linha, 7).text()
        REMOVE.DelItem()
        self.tb_Itens.removeRow(linha)
        for row in range(self.tb_Itens.rowCount()):
            self.botaoRemoveItem(self.tb_Itens, row, 6,
                                 partial(self.RemoveLInha, row), "#005099")
        self.TotalFinal()
        self.bt_GerarParcelaVenda.setDisabled(True)

        # Desativando Botões
    def DesativaBotaoVendas(self):
        self.bt_AddNovoVenda.setEnabled(False)
        self.tx_BuscaVendas.setEnabled(False)
        self.bt_BuscaVendas.setEnabled(False)

    def AtivaBotaoVendas(self):
        self.bt_AddNovoVenda.setEnabled(True)
        self.tx_BuscaVendas.setEnabled(True)
        self.bt_BuscaVendas.setEnabled(True)

    def LimpaCampoAddProduto(self):
        for filho in self.fr_addProduto.findChildren(QtWidgets.QLineEdit):
            filho.clear()
        self.bt_IncluirItemPedido.setDisabled(True)
        self.tx_IdBuscaItem.setFocus()

        # Salvar Venda
    def validaCad(self):
        if self.cb_FormaPagamentoVenda.currentIndex() == 0:
            self.cb_FormaPagamentoVenda.setFocus()
        elif self.cb_ParcelamentoVenda.currentIndex() == 0:
            self.cb_ParcelamentoVenda.setFocus()
        elif self.tb_parcelasVenda.rowCount() < 1:
            self.cb_ParcelamentoVenda.setFocus()

        else:
            self.CadVenda()

    # Gerar parcela
    def gerarParcela(self):
        numParcela = self.cb_ParcelamentoVenda.currentIndex()
        valorTotal = self.tx_TotalFinal.text()
        valor_parcela = float(valorTotal) / int(numParcela)

        while self.tb_parcelasVenda.rowCount() > 0:
            self.tb_parcelasVenda.removeRow(0)
            pass
        for i in range(numParcela):

            self.tb_parcelasVenda.insertRow(i)
            # self.conteudoTabela(self.tb_parcelasVenda, i, 0, str(i + 5))
            # self.conteudoTabelaLeft(self.tb_parcelasVenda, i, 1, QtCore.QDate.toString(
            # QtCore.QDate.addMonths(self.dt_VencimentoVenda.date(), i),
            # 'dd-MM-yyyy'))
            self.dt_tabela(self.tb_parcelasVenda, i, 1, QtCore.QDate.addMonths(
                self.dt_VencimentoVenda.date(), i), 2)
            self.conteudoTabela(self.tb_parcelasVenda, i, 2,
                                format(valor_parcela, ".2f"))
            self.botaoReceberParcela(self.tb_parcelasVenda, i, 4,
                                     partial(self.Receber, i), "Receber", 1)
            self.tx_tabelaReceber(self.tb_parcelasVenda, i, 3, 2, '')

        pass

    def CadVenda(self):
        if not int(self.tb_Itens.rowCount()) < 1:
            INSERI = CrudPedidos()
            INSERI.idPedido = self.tx_CodPedido.text()
            INSERI.idCliente = self.tx_CodClienteVenda.text()
            INSERI.dataEmissao = QtCore.QDate.toString(
                self.dt_EmissaoPedido.date(), 'yyyy-MM-dd')
            INSERI.prazoEntrega = QtCore.QDate.toString(
                self.dt_PrazoEntrega.date(), 'yyyy-MM-dd')
            INSERI.desconto = self.tx_Desconto.text()
            INSERI.frete = self.tx_Frete.text()
            INSERI.valorTotal = self.tx_TotalFinal.text()
            if float(self.lb_ValorPendente.text()) == 0:
                INSERI.statusPagamento = 1
            else:
                INSERI.statusPagamento = 2
            INSERI.valorPendente = self.lb_ValorPendente.text()
            INSERI.CadVenda()
            self.CadItemVenda()

        pass

    def CadItemVenda(self):
        INSERI = CrudPedidos()
        i = 0
        while i < self.tb_Itens.rowCount():
            INSERI.idItem = self.tb_Itens.item(i, 0).text()
            INSERI.idPedido = self.tx_CodPedido.text()
            INSERI.idItemTabela = self.tb_Itens.item(i, 7).text()
            INSERI.qtde = self.tb_Itens.item(i, 3).text()
            INSERI.valorItem = self.tb_Itens.item(i, 4).text()
            INSERI.totalItem = self.tb_Itens.item(i, 5).text()
            INSERI.obsItem = self.tb_Itens.item(i, 2).text()
            INSERI.CadItensPedido()
            i += 1

        self.CadContaVenda()
        self.SelectVendaId(self.tx_CodPedido.text())

        pass

    def CadContaVenda(self):
        INSERI = CrudAReceber()

        if self.tb_parcelasVenda.rowCount() > 0:
            for i in range(self.tb_parcelasVenda.rowCount()):
                try:
                    self.tb_parcelasVenda.item(i, 0).text()
                    INSERI.idConta = self.tb_parcelasVenda.item(i, 0).text()
                except:
                    INSERI.idConta = ''
                INSERI.idVenda = self.tx_CodPedido.text()
                INSERI.idCliente = self.tx_CodClienteVenda.text()
                INSERI.descricao = """Pedido de Venda {}. Parcela {} de {} """.format(
                    self.tx_CodPedido.text(), i + 1, self.tb_parcelasVenda.rowCount())
                INSERI.obs = ""
                INSERI.categoria = 1
                INSERI.dataVencimento = QtCore.QDate.toString(
                    self.tb_parcelasVenda.cellWidget(i, 1).date(), "yyyy-MM-dd")
                INSERI.valor = self.tb_parcelasVenda.item(i, 2).text()
                INSERI.formaPagamento = self.cb_FormaPagamentoVenda.currentIndex()
                INSERI.cadContaReceber()

    # Validar valor Recebido
    def validarRecebimento(self):
        valorRecebido = float(self.tx_ValorPago.text().replace(',', '.'))
        valorPendente = float(self.lb_ValorPendente.text().replace(',', '.'))
        if valorRecebido > valorPendente:
            self.tx_ValorPago.setText(format(valorPendente, '.2f'))

    # Recebendo pagamento DB
    def Receber(self, id):
        # print(self.tb_parcelasVenda.item(id, 0).text())

        if self.tb_parcelasVenda.cellWidget(id, 3).text():
            INSERI = CrudAReceber()
            INSERI.idConta = self.tb_parcelasVenda.item(id, 0).text()
            INSERI.valorRecebido = self.tb_parcelasVenda.cellWidget(
                id, 3).text().replace(",", ".")

            INSERI.dataRecebimento = QtCore.QDate.toString(
                QtCore.QDate.currentDate(), "yyyy-MM-dd")
            # if float(self.tb_parcelasVenda.cellWidget(id, 3).text().replace(",", ".")) < float(self.tb_parcelasVenda.item(id, 2).text().replace(",", ".")):
            #     INSERI.status = 2
            # else:
            #     INSERI.status = 1

            INSERI.cadContaReceber()
            self.ParcelasAReceber()

    # Entregando pedido DB
    def Entregar(self):
        INSERI = CrudPedidos()
        INSERI.dataEntrega = QtCore.QDate.toString(
            self.dt_EntregaPedido.date(), "yyyy-MM-dd")
        INSERI.idPedido = self.tx_CodPedido.text()
        INSERI.Entregar()
        self.SaidaEstoque()
        self.SelectVendaId(self.tx_CodPedido.text())

    # Dando Entrada no Estoque
    def SaidaEstoque(self):
        INSERI = CrudProdutos()
        i = 0
        while i < self.tb_Itens.rowCount():
            INSERI.idProduto = self.tb_Itens.item(i, 0).text()
            INSERI.idRelacao = self.tb_Itens.item(i, 7).text()
            INSERI.qtdeProduto = self.tb_Itens.item(i, 3).text()
            INSERI.data = QtCore.QDate.toString(
                QtCore.QDate.currentDate(), 'yyyy-MM-dd')

            INSERI.SaidaProduto()
            i += 1

    # Selecionando Venda pela tabela
    def SelectVendaId(self, id):
        busca = CrudPedidos()
        self.FormVendas()
        self.tx_CodPedido.setText(str(id))
        busca.SelectVendaID(id)

        self.tx_CodClienteVenda.setText(str(busca.idCliente))
        self.BuscaClienteId()
        self.tx_Desconto.setText(str(busca.desconto))
        self.tx_Frete.setText(str(busca.frete))
        self.dt_PrazoEntrega.setDate(busca.prazoEntrega)
        if busca.valorRecebido:
            self.tx_valorRecebido.setText(str(busca.valorRecebido))
        if busca.statusPagamento == 2:
            self.bt_GerarParcelaVenda.setEnabled(True)
        if busca.statusEntrega == 2:
            self.bt_Entregar.setEnabled(True)
        if busca.statusPagamento == 1 or busca.statusEntrega == 1:
            self.tb_Itens.setColumnHidden(6, True)
            # self.bt_SalvarVenda.setDisabled(True)
            for item in self.fr_addProduto.findChildren(QtWidgets.QLineEdit):
                item.setReadOnly(True)

        i = 0
        while i < len(busca.itemDescricao):

            self.tb_Itens.insertRow(i)
            self.conteudoTabela(self.tb_Itens, i, 0,
                                str(busca.idItem[i]))
            self.conteudoTabelaLeft(self.tb_Itens, i, 1,
                                    busca.itemDescricao[i])
            self.conteudoTabelaLeft(self.tb_Itens, i, 2,
                                    str(busca.obsItem[i]))
            self.conteudoTabela(self.tb_Itens, i, 3,
                                str(busca.qtde[i]))
            self.conteudoTabela(self.tb_Itens, i, 4,
                                str(busca.valorItem[i]))
            self.conteudoTabela(self.tb_Itens, i, 5,
                                str(busca.totalItem[i]))
            self.botaoRemoveItem(self.tb_Itens, i, 6,
                                 partial(self.RemoveLInha, i), "#005099")
            self.conteudoTabela(self.tb_Itens, i, 7,
                                str(busca.idItemTabela[i]))
            self.TotalFinal()

            i += 1
        self.bt_ImprimirVenda.setEnabled(True)
        self.ParcelasAReceber()

        pass

    def ParcelasAReceber(self):
        while self.tb_parcelasVenda.rowCount() > 0:
            self.tb_parcelasVenda.removeRow(0)

        busca = CrudAReceber()
        busca.idVenda = self.tx_CodPedido.text()
        busca.selectAReceberId()

        if busca.dataVencimento:
            self.bt_GerarParcelaVenda.setDisabled(True)

        for i in range(len(busca.dataVencimento)):
            self.tb_parcelasVenda.insertRow(i)
            self.conteudoTabela(self.tb_parcelasVenda, i,
                                0, str(busca.idConta[i]))
            self.dt_tabela(self.tb_parcelasVenda, i,
                           1, busca.dataVencimento[i], busca.idStatus[i])
            self.conteudoTabela(self.tb_parcelasVenda, i,
                                2, str(busca.valor[i]))
            self.tx_tabelaReceber(self.tb_parcelasVenda, i, 3, busca.idStatus[
                                  i], str(busca.valor[i] - busca.valorRecebido[i]))
            self.botaoReceberParcela(self.tb_parcelasVenda, i, 4,
                                     partial(self.Receber, i), "Receber", busca.idStatus[i])

        # self.bt_GerarParcelaVenda.setDisabled(True)

    def imprimirVenda(self):
        self.documento = QWebEngineView()

        headertable = ["Produto", "Obs. ", "Qnte.", "$ Unitário", "$ Total"]
        buscaFornecedor = CrudClientes()
        buscaFornecedor.ListaClientesTabela('')
        html = self.renderTemplate(
            "venda.html",
            estilo=self.resourcepath('Template/estilo.css'),
            titulo="Pedido Nº:",
            idPedido=self.tx_CodPedido.text(),
            headertable=headertable,
            codcliente=buscaFornecedor.idCliente,
            nomeCliente=buscaFornecedor.nomeCliente,
            telefoneFornecedor=buscaFornecedor.celularCliente,
            emailFornecedor=buscaFornecedor.emailCliente
        )

        self.documento.load(QtCore.QUrl("file:///" +
                                        self.resourcepath("report.html")))
        self.documento.loadFinished['bool'].connect(self.previaImpressao)