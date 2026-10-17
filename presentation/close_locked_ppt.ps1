$ppt = [System.Runtime.InteropServices.Marshal]::GetActiveObject('PowerPoint.Application')
if ($ppt) {
    foreach ($pres in $ppt.Presentations) {
        Write-Host "Open presentation:" $pres.Name "at" $pres.FullName
        if ($pres.Name -like "*SafeRoads*") {
            Write-Host "Closing presentation:" $pres.Name
            $pres.Close()
        }
    }
}
