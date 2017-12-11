import QtQuick 2.8
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

ColumnLayout {

    RowLayout {
        id: topPane
        Layout.fillWidth: true
        anchors.top: parent.top

        Text {
            text: "Welcome to StockSim!"
            Layout.fillWidth: true
        }

        Button {
            id: loadData
            text: "Load Data"
        }

        Button {
            id: saveData
            text: "Save Data"
        }
    }

    RowLayout {
        id: rowLayout
        Layout.fillHeight: true
        Layout.fillWidth: true

        ColumnLayout {
            id: leftPane
            Layout.fillHeight: true
            anchors.left: parent.left

            ScrollView {
                Layout.minimumHeight: 100
                anchors.top: parent.top
                Layout.fillHeight: true

                ListView {
                    id: listView
                    x: 0
                    y: 0
                    width: 110
                    highlight: Rectangle {
                        color: "lightsteelblue"
                    }
                    model: ListModel {
                        ListElement {
                            name: "Grey"
                            colorCode: "grey"
                        }

                        ListElement {
                            name: "Red"
                            colorCode: "red"
                        }

                        ListElement {
                            name: "Blue"
                            colorCode: "blue"
                        }

                        ListElement {
                            name: "Green"
                            colorCode: "green"
                        }
                    }
                    delegate: Item {
                        x: 5
                        width: 80
                        height: 40
                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onClicked: listView.view.currentIndex = index
                        }

                        Row {
                            id: row1
                            x: 0
                            y: 0
                            spacing: 10
                            Rectangle {
                                width: 40
                                height: 40
                                color: colorCode
                            }

                            Text {
                                text: name
                                font.bold: true
                                anchors.verticalCenter: parent.verticalCenter
                            }
                        }
                    }
                }
            }

            Button {
                id: addStock
                text: "Add"
            }

            Button {
                id: loadStock
                text: "Load"
            }

            Button {
                id: exportStock
                text: "Export"
            }

            Button {
                id: deleteStock
                text: "Delete"
                anchors.bottom: parent.bottom
            }
        }
        ColumnLayout {
            id: rightPane
            Layout.fillHeight: true
            Layout.fillWidth: true
            anchors.right: parent.right

            TabBar {
                id: bar
                anchors.top: parent.top
                anchors.right: parent.right

                TabButton {
                    text: qsTr("History")
                }

                TabButton {
                    text: qsTr("Transactions")
                }

                TabButton {
                    text: qsTr("Value")
                }
            }

            StackLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                anchors.bottom: parent.bottom
                currentIndex: bar.currentIndex

                ColumnLayout {
                    id: historyTab
                    anchors.bottom: parent.bottom

                    ScrollView {
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        TextArea {
                            id: historyData
                            text: qsTr("History data")
                        }
                    }

                    RowLayout {
                        anchors.bottom: parent.bottom
                        anchors.right: parent.right

                        Button {
                            id: openHistory
                            text: qsTr("Open file")
                            onClicked: {
                                stocksim.open_history()
                            }
                        }
                        Button {
                            id: loadHistory
                            text: qsTr("Load")
                            onClicked: {
                                stocksim.load_history(historyData.text)
                                statusBar.text = "History loaded"
                                statusBar.update()
                            }
                        }
                    }
                }

                ColumnLayout {
                    id: transactionsTab

                    RowLayout {
                        Layout.fillWidth: true

                        RadioButton {
                            id: shares
                            text: qsTr("Shares")
                        }

                        RadioButton {
                            id: cash
                            text: qsTr("Cash")
                        }
                    }

                    TextArea {
                        id: transactionData
                        text: "Transactions"
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                    }

                    RowLayout {
                        Button {
                            id: openTransactions
                            text: qsTr("Open file")
                        }
                        Button {
                            id: loadTransactions
                            text: qsTr("Load")
                            onClicked: {
                                stocksim.load_transactions(transactionData.text)
                                statusBar.text = "Transactions loaded"
                                statusBar.update()
                            }
                        }
                    }
                }

                ColumnLayout {
                    id: valueTab

                    RowLayout {
                        ColumnLayout {
                            Text {
                                text: qsTr("Shares")
                            }
                            TextArea {
                                id: sharesData
                                Layout.fillHeight: true
                                Layout.fillWidth: true
                            }
                        }
                        ColumnLayout {
                            Text {
                                text: qsTr("Value")
                            }
                            TextArea {
                                id: valueData
                                Layout.fillHeight: true
                                Layout.fillWidth: true
                            }
                        }
                    }
                    Button {
                        id: calcValue
                        text: "Calculate"
                        onClicked: {
                            stocksim.calc_stock_shares(0)
                            stocksim.calc_stock_value(0)

                            sharesData.update()
                            valueData.update()
                            statusBar.text = "Value data updated"
                            statusBar.update()
                        }
                    }
                }
            }
        }
    }

    Text {
        id: statusBar
        text: qsTr("Ready")
        Layout.fillWidth: true
        anchors.bottom: parent.bottom
    }

    function update_history(data){}
}
