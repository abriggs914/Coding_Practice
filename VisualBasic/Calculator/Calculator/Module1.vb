Module Module1

    Public Enum FunctionsEnum
        QUIT
        CLEAR_CURR_VAL
        CHANGE_CURR_VALUE
        CHANGE_CURR_MEMORY_VAL
        ADD_TO_MEMORY_VAL
        CLEAR_MEMORY_VAL
        CHANGE_CURR_FUNCTION
        ADDITION
        SUBTRACTION
        MULTIPLICATION
        DIVISION
        POWER
        LOG
        SQRT
    End Enum

    Dim MinimumFunctions As List(Of FunctionsEnum) = New List(Of FunctionsEnum)({
                                                                                FunctionsEnum.QUIT,
                                                                                FunctionsEnum.CLEAR_CURR_VAL,
                                                                                FunctionsEnum.CHANGE_CURR_VALUE,
                                                                                FunctionsEnum.CHANGE_CURR_MEMORY_VAL,
                                                                                FunctionsEnum.ADD_TO_MEMORY_VAL,
                                                                                FunctionsEnum.CLEAR_MEMORY_VAL,
                                                                                FunctionsEnum.CHANGE_CURR_FUNCTION
                                                                                })

    Dim Border As String = "##################################################"

    Dim ValidUserAgrees As List(Of String) = New List(Of String)({"n", "N", "y", "Y"})

    Dim BorderChar As String = "#"

    Public Class Calculator
        Public Property CurrVal As Double
        Public Property CurrFunction As FunctionsEnum
        Public Property MemoryVal As Double
        Public Property History As List(Of Double)
        Public Property Functions As List(Of FunctionsEnum)

        Public Sub New(ByRef Funcs As FunctionsEnum())
            Me.CurrVal = 0
            Me.MemoryVal = 0
            Me.History = New List(Of Double)
            Me.Functions = New List(Of FunctionsEnum)
            Me.Functions.AddRange(MinimumFunctions)
            Dim c As Integer = 0
            'For i As Integer = 0 To MinimumFunctions.Count - 1
            '    Dim fe As FunctionsEnum = MinimumFunctions(MinimumFunctions.Count - i - 1)
            '    If Not Funcs.Contains(fe) Then
            '        Me.Functions.Insert(0, fe)
            '        i += 1
            '    End If
            'Next
            For Each func In Funcs
                If Not Functions.Contains(func) Then
                    Me.Functions.Add(func)
                End If
            Next
            d = "Avery"
        End Sub

        Public Sub Greeting()
            Dim message As String = String.Empty
            message += vbNewLine & Border
            message += vbNewLine & vbTab & "Welcome to the Calculator!" & vbNewLine
            message += "We currently support:" & vbNewLine
            For Each func In Functions
                message += vbTab & "-" & vbTab & Title(func.ToString()) & vbNewLine
            Next
            message += vbNewLine & "Enter a number to get started:"
            message += vbNewLine & Border & vbNewLine
            Console.WriteLine(message)
            UpdateCurrVal(GetNumberInput())
        End Sub

        Public Sub Run()
            Greeting()
            Dim Looping As Boolean = True
            Do
                ' get operation
                ChangeCurrFunction()
                Dim operandB As Double = 0
                Select Case CurrFunction
                    Case FunctionsEnum.QUIT
                        Quit()
                        Looping = False
                    Case FunctionsEnum.CHANGE_CURR_VALUE
                        ChangeCurrVal()
                    Case FunctionsEnum.CHANGE_CURR_MEMORY_VAL
                        ChangeCurrMemoryVal()
                    Case FunctionsEnum.ADD_TO_MEMORY_VAL
                        AddToCurrMemoryVal()
                    Case FunctionsEnum.CLEAR_MEMORY_VAL
                        ClearCurrMemoryVal()
                    Case FunctionsEnum.CHANGE_CURR_FUNCTION
                        ChangeCurrFunction()
                    Case FunctionsEnum.ADDITION
                        operandB = GetNumberInput()
                        UpdateCurrVal(Addition(CurrVal, operandB))
                    Case FunctionsEnum.SUBTRACTION
                        operandB = GetNumberInput()
                        UpdateCurrVal(Subtraction(CurrVal, operandB))
                    Case FunctionsEnum.MULTIPLICATION
                        operandB = GetNumberInput()
                        UpdateCurrVal(Multiplication(CurrVal, operandB))
                    Case FunctionsEnum.DIVISION
                        operandB = GetNumberInput()
                        UpdateCurrVal(Division(CurrVal, operandB))
                    Case FunctionsEnum.POWER
                        operandB = GetNumberInput()
                        UpdateCurrVal(Power(CurrVal, operandB))
                    Case FunctionsEnum.LOG
                        UpdateCurrVal(Log(CurrVal))
                    Case FunctionsEnum.SQRT
                        UpdateCurrVal(Sqrt(CurrVal))
                    Case Else
                        Console.WriteLine("Operation not recognized")
                End Select

            Loop Until Not Looping
        End Sub

        Public Sub Quit()
            Console.WriteLine(Border & vbNewLine & PadCentre("Bye!", Border.Length) & vbNewLine & Border)
        End Sub

        Public Sub ChangeCurrFunction()
            Dim input As Double
            Dim agrees As Boolean = False
            Dim lst As List(Of FunctionsEnum) = [Enum].GetValues(GetType(FunctionsEnum)).Cast(Of FunctionsEnum)().ToList()
            Do
                Console.Clear()
                ShowCurrVal()
                If MemoryVal Then
                    ShowMemoryVal()
                End If
                ShowOptions()
                input = GetNumberInput()
                agrees = UserAgrees("(" & input & ") - Are you sure?")
                Console.WriteLine("Function chosen (" & lst.Count() & "): " & lst.ToString() & " -> " & lst(input))
            Loop Until agrees
            UpdateCurrFunction(lst(input))
        End Sub

        Public Sub ClearCurrMemoryVal()
            UpdateMemoryVal(Nothing)
        End Sub

        Public Sub AddToCurrMemoryVal()
            UpdateMemoryVal(CurrVal)
        End Sub

        Public Sub ChangeCurrMemoryVal()
            Dim input As Double = GetNumberInput()
            UpdateMemoryVal(input)
        End Sub

        Public Sub ChangeCurrVal()
            Dim input As Double = GetNumberInput()
            UpdateCurrVal(input)
        End Sub

        Public Sub UpdateCurrVal(ByVal value As Double)
            Me.CurrVal = value
            Me.History.Add(value)
        End Sub

        Public Sub UpdateMemoryVal(ByVal value As Double)
            Me.MemoryVal = value
        End Sub

        Public Sub UpdateCurrFunction(ByVal func As FunctionsEnum)
            Me.CurrFunction = func
        End Sub

        Public Sub ShowCurrVal()
            'Console.WriteLine("currVal: " & CurrVal)
            'Console.WriteLine(CurrVal.GetType())
            'Console.WriteLine(CurrVal.ToString())
            'Console.ReadLine()
            'Dim s As String = CurrVal.ToString()
            Dim n As Integer = Str(CurrVal).Length
            Dim b As Integer = Border.Length - 3
            Dim val As String = BorderChar & Str(CurrVal).PadLeft(b).PadRight(b + 1) & BorderChar
            Console.WriteLine(Border)
            Console.WriteLine(val)
            Console.WriteLine(Border)
        End Sub

        Public Sub ShowMemoryVal()
            Dim n As Integer = Str(MemoryVal).Length
            Dim b As Integer = Border.Length - 3
            Dim val As String = BorderChar & Str(MemoryVal).PadLeft(b).PadRight(b + 1) & BorderChar
            Console.WriteLine(Border)
            Console.WriteLine(val)
            Console.WriteLine(Border)
        End Sub

        Public Sub ShowOptions()
            Dim m As String = String.Empty
            Dim l As Integer = Functions.Count - 1
            Dim numSpacer As String = "    "
            Dim numPad As Integer = 5
            Dim numSpaceChar As String = "-"
            Dim b As Integer = Border.Length - 3 - numSpacer.Length - numPad - numSpaceChar.Length
            For i As Integer = 0 To l
                Dim line As String = numSpacer & Str(i).PadRight(numPad) & numSpaceChar
                line += Functions(i).ToString.PadLeft(b)
                m += "#" & line & " #" & If((i < l), vbNewLine, "")
            Next
            m = BorderChar & PadCentre("Select an operation to perform:", Border.Length - 2) & BorderChar & vbNewLine & m
            Console.WriteLine(Border)
            Console.WriteLine(m)
            Console.WriteLine(Border)
        End Sub

        ' Operation functions

        Public Function Addition(ByVal a As Double, ByVal b As Double) As Double
            Return a + b
        End Function

        Public Function Subtraction(ByVal a As Double, ByVal b As Double) As Double
            Return a - b
        End Function

        Public Function Multiplication(ByVal a As Double, ByVal b As Double) As Double
            Return a * b
        End Function

        Public Function Division(ByVal a As Double, ByVal b As Double) As Double
            Return a / b
        End Function

        Public Function IntDivision(ByVal a As Double, ByVal b As Double) As Double
            Return a \ b
        End Function

        Public Function Power(ByVal a As Double, ByVal b As Double) As Double
            Return a ^ b
        End Function

        Public Function Sqrt(ByVal a As Double) As Double
            Return a ^ 0.5
        End Function

        Public Function Log(ByVal a As Double) As Double
            Return Math.Log(a)
        End Function

    End Class

    Public Function Title(ByVal Text As String) As String
        Dim res As String = String.Empty
        Dim arr As Char() = Text.ToCharArray
        For i As Integer = 0 To arr.Length - 1
            Dim cVal As Integer = AscW(arr(i))
            If i > 0 Then
                If 64 < cVal And cVal < 91 Then
                    cVal += 32
                End If
            Else
                If 96 < cVal And cVal < 123 Then
                    cVal -= 32
                End If
            End If
            Dim c As Char = ChrW(cVal)
            res += c.ToString
        Next
        Return res
    End Function

    Public Function PadCentre(ByVal Text As String, ByVal PadStr As String, ByVal len As Integer) As String
        If len > 0 Then
            Dim h As Integer = (len - Text.Length) \ 2
            Dim odd As Boolean = (((2 * h) + Text.Length) = len)
            Text = Text.PadRight(h + Text.Length, PadStr)
            h += If(Not odd, 1, 0)
            Text = Text.PadLeft(h + Text.Length, PadStr)
            Return Text
        Else
            Return ""
        End If
    End Function

    Public Function PadCentre(ByVal Text As String, ByVal len As Integer) As String
        Return PadCentre(Text, " ", len)
    End Function

    Public Function GetNumberInput()
        Console.WriteLine("Enter a double value" & vbNewLine)
        Dim input As String = Console.ReadLine()
        Dim num As Double = 0
        If Double.TryParse(input, num) Then
            Return num
        End If
        Return num
    End Function

    ' Return a double from console input
    Public Function GetInput() As String
        Console.WriteLine("Enter a value" & vbNewLine)
        Dim input As String = Console.ReadLine()
        Return input
    End Function

    Public Function Wrap(ByVal Text As String, ByVal len As Integer) As List(Of String)
        Dim res As List(Of String) = New List(Of String)
        If len < 2 Then
            Return res
        End If
        'Dim n As Integer = Math.Min(Text.Length, len)
        Dim chars As Char() = Text.ToCharArray
        Dim line As String = " "
        For i As Integer = 0 To Text.Length - 1
            line += chars(i)
            If line.Length = len Then
                res.Add(line)
                line = String.Empty
            End If
        Next
        If line.Length > 0 Then
            res.Add(line.PadRight(Border.Length - 3))
        End If
        Return res
    End Function

    Public Function UserAgrees(ByVal Message As String) As Boolean
        Dim ValidInput As Boolean = False
        Dim input As String
        Dim emptyLine As String = BorderChar & "".PadRight(Border.Length - 2) & BorderChar
        Do
            Console.WriteLine(Border)
            Dim messageLines As List(Of String) = Wrap(Message, Border.Length - 2)
            For Each line In messageLines
                Console.WriteLine("#" & line & " #")
            Next
            Console.WriteLine(emptyLine & vbNewLine & BorderChar & PadCentre("Do you agree?", Border.Length - 2) & BorderChar)
            Console.WriteLine(emptyLine & vbNewLine & BorderChar & PadCentre("Y for yes / N for No", Border.Length - 2) & BorderChar)
            Console.WriteLine(Border)
            input = GetInput()
            ValidInput = ValidUserAgrees.Contains(input)
        Loop Until ValidInput
        If ValidUserAgrees.IndexOf(input) < 2 Then
            ' User disagrees
            Return False
        Else
            Return True
        End If
    End Function

    Sub Main()

        'Dim a As Boolean = UserAgrees("Testing?")
        Dim funcs As FunctionsEnum() = New FunctionsEnum() {FunctionsEnum.ADDITION, FunctionsEnum.SUBTRACTION, FunctionsEnum.MULTIPLICATION, FunctionsEnum.DIVISION, FunctionsEnum.POWER, FunctionsEnum.LOG, FunctionsEnum.SQRT}
        Dim Calculator As Calculator = New Calculator(funcs)
        Calculator.Run()
        'Dim a As String = "1234567"
        'Dim b As String = "12345678"
        'Dim l As Integer = 15
        'Dim c As String = "*"
        'Console.WriteLine("a: {" & PadCentre(a, c, l) & "} (" & PadCentre(a, c, l).Length & ")")
        'Console.WriteLine("b: {" & PadCentre(b, c, l) & "} (" & PadCentre(b, c, l).Length & ")")
        'Console.ReadLine()
    End Sub

End Module
