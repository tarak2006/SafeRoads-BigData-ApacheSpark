$pptApp = New-Object -ComObject PowerPoint.Application
$pptFile = "E:\Bigdata_review3\presentation\SafeRoads_ApacheSpark_CaseStudy_Improvised.pptx"
$pres = $pptApp.Presentations.Open($pptFile, 1, 0, 0)
$outDir = "E:\Bigdata_review3\presentation\slide_images"
if (!(Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir }
$pres.Slides.Item(11).Export($outDir + "\slide_11.png", "PNG", 1920, 1080)
$pres.Close()
$pptApp.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($pptApp) | Out-Null
Write-Host "SUCCESS_EXPORT"
