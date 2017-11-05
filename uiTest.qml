import QtQuick 2.8
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

ColumnLayout {
    Text {
        text: "Welcome to StockSim!"
    }
    RowLayout {
        id: rowLayout
        ListView {
            id: listView
            width: 110
            height: 260
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
                Row {
                    id: row1
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
        ColumnLayout {

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
            }
        }
    }
}
