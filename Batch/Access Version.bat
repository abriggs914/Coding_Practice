if exist "C:\Program Files\Microsoft Office\root\Office16\MSACCESS.EXE" (
	echo "You have Access version 10, 13, 16, or 19"
) else (
	if exist "C:\Program Files (x86)\Microsoft Office\Office12\MSACCESS.EXE" (
		echo "You have Access version 7"
	) else (
		echo "Other"
	)
)
pause