import QtQuick 2.0
import QtQuick.Dialogs 1.2

FileDialog {
    id: fileDialog
    objectName: "fileDialog"
    title: "Please choose a file"
    modality: Qt.ApplicationModal
    onAccepted: {
        console.log("You chose: " + fileDialog.fileUrls)
        Qt.quit()
    }
    onRejected: {
        console.log("Canceled")
        Qt.quit()
    }
    // Component.onCompleted: visible = true
}
