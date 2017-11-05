import QtQuick 2.8
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

ColumnLayout {
    RowLayout {
        id: topPane
        Text {
            text: "Welcome to StockSim!"
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

        Column {
            id: leftPane
            width: 200
            height: 400

            ListView {
                id: listView
                width: 110
                height: 260
                highlight: Rectangle { color: "lightsteelblue" }
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
            }
        }
        ColumnLayout {
            id: rightPane

            TabBar {
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

                ColumnLayout {
                    id: historyTab

                    TextArea {
                        id: textArea
                        text: qsTr("Text Area")
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                    }

                    RowLayout {
                        Button {
                            text: qsTr("Open file")
                        }
                        Button {
                            text: qsTr("Load")
                        }
                    }
                }

                ColumnLayout {
                    id: transactionsTab

                    TextArea {
                        text: "Transactions"
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                    }

                    RowLayout {
                        Button {
                            text: qsTr("Open file")
                        }
                        Button {
                            text: qsTr("Load")
                        }
                    }
                }
            }
        }
    }
}
