Private Sub Detail_Format(Cancel As Integer, FormatCount As Integer)

    If IsNull(Me.Application_txt) Then
        Me.GH1Hide.Caption = 1
    Else
        Me.GH1Hide.Caption = 0
    End If
    
    If Me.GH1Hide.Caption = 0 Then
        Detail.Visible = True
    Else
        Detail.Visible = False
    End If

    If CurrentProject.AllForms("SYSPROJob").IsLoaded = False Then
        Debug.Print """SYSPROJob"" IS not loaded."
        'DoCmd.OpenForm "SYSPROJob"
    End If

    Dim Job As String
    'DoCmd.RunSQL "SELECT TOP 1 [Job] FROM [dtSYSPROWOLabourandMaterials];"
    'Job = [Forms]![SYSPROJob]![Job]
    'DoCmd.Close acForm, "SYSPROJob"
    
    'If Not Me.Job Is Nothing Then
    '    If Not IsNull(Me.Job) Then
    '        If Not IsEmpty(Me.Job) Then
                'Dim a As Integer
                For Each FLD In Me.Recordset.FieldNames
                    Debug.Print "a: <" & a & ">"
                Next FLD
                
                'Debug.Print "Len(Me.Job): <" & Len([Forms]![SYSPROJob]![Job]) & ">"
                'Debug.Print "Len(Me.Job): <" & [Tables]![dtSYSPROWOLabourandMaterials] & ">"
                'Debug.Print "Me.Job: <" & [Forms]![SYSPROJob]![Job] & ">"
                'Debug.Print "Len(Me.Job): <" & Len(Me.Job) & ">"
                'Debug.Print "Me.Job: <" & Me.Job & ">"
                If Me.Job Like "5*" Then
                    Me.Label130.Visible = True
                    Me.Text129.Visible = True
                Else
                    Me.Label130.Visible = False
                    Me.Text129.Visible = False
                End If
     '       End If
     '   End If
    'End If
    
End Sub