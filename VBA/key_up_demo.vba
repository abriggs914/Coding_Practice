Private Sub Text22_KeyUp(KeyCode As Integer, Shift As Integer)
    DoCmd.SetWarnings False
    Dim cn As String
    If IsNull(Me.CompanyName) Then
        'MsgBox "Please select a company first."
        Exit Sub
    End If
    cn = Me.CompanyName
    Debug.Print vbTab & "keycode <" & KeyCode & ">"
    If KeyCode = vbKey1 Or KeyCode = vbKey2 Or KeyCode = vbKey3 Or KeyCode = vbKey4 Or KeyCode = vbKey5 Or KeyCode = vbKey6 Or KeyCode = vbKey7 Or KeyCode = vbKey8 Or KeyCode = vbKey9 Or KeyCode = vbKey0 Or KeyCode = 96 Or KeyCode = 97 Or KeyCode = 98 Or KeyCode = 99 Or KeyCode = 100 Or KeyCode = 101 Or KeyCode = 102 Or KeyCode = 103 Or KeyCode = 104 Or KeyCode = 105 Then
        Select Case KeyCode
            Case 96: KeyCode = vbKey0
            Case 97: KeyCode = vbKey1
            Case 98: KeyCode = vbKey2
            Case 99: KeyCode = vbKey3
            Case 100: KeyCode = vbKey4
            Case 101: KeyCode = vbKey5
            Case 102: KeyCode = vbKey6
            Case 103: KeyCode = vbKey7
            Case 104: KeyCode = vbKey8
            Case 105: KeyCode = vbKey9
        End Select
            
        Debug.Print "KEY PRESSED!!!"
        Dim qdf As DAO.QueryDef
        Dim rs As DAO.Recordset
        Dim db As DAO.Database
        Set db = CurrentDb
        Set qdf = db.QueryDefs("Dealer Slots Per Month New Data")
        qdf.SQL = "SELECT ID FROM Dealers WHERE [COMPANY NAME]='" & cn & "'"
        Set rs = db.OpenRecordset(qdf.Name, dbOpenSnapshot)
        If rs.BOF Or rs.EOF Then
            Debug.Print "No Data Returned."
        Else
            Dim txtVal As String
            If Me.Text22 = "0" Then
                txtVal = Chr(KeyCode)
            End If
            txtVal = Me.Text22 & Chr(KeyCode)
            Debug.Print "txtVal: <" & txtVal & "> keycode <" & Chr(KeyCode) & "> Value <" & Me.Text22 & ">" & vbTab & "Query:" & vbNewLine & "UPDATE [Dealers] SET [SlotsRequestedPerMonth] = " & Me.Text22 & " WHERE [COMPANY NAME] = """ & Me.CompanyName & """"
            DoCmd.RunSQL "UPDATE [Dealers] SET [SlotsRequestedPerMonth] = " & txtVal & " WHERE [ID] = " & rs(0).Value & ";"
        End If
    End If

End Sub
