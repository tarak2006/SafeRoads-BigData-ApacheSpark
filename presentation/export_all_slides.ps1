$pptApp = New-Object -ComObject PowerPoint.Application
$pptFile = "E:\Bigdata_review3\presentation\SafeRoads_ApacheSpark_Review3_Fitted.pptx"
$pres = $pptApp.Presentations.Open($pptFile, 1, 0, 0)
$outDir = "E:\Bigdata_review3\presentation\slide_images"
if (!(Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir }

for ($i = 1; $i -le $pres.Slides.Count; $i++) {
    $pres.Slides.Item($i).Export("$outDir\slide_$i.png", "PNG", 1920, 1080)
}
$pres.Close()
$pptApp.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($pptApp) | Out-Null
Write-Host "ALL_FITTED_SLIDES_EXPORTED"
