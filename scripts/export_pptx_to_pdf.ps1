$pptx = (Resolve-Path "MONSOON_PULSE_ARCHON.pptx").Path
$pdf = [System.IO.Path]::ChangeExtension($pptx, ".pdf")

Write-Host "Converting PPTX to PDF..."
Write-Host "Input:  $pptx"
Write-Host "Output: $pdf"

$ppt = New-Object -ComObject PowerPoint.Application
try {
    # Open(FileName, ReadOnly, Untitled, WithWindow)
    $pres = $ppt.Presentations.Open($pptx, 0, 0, 0)
    # SaveAs(FileName, ppSaveAsPDF=32)
    $pres.SaveAs($pdf, 32)
    $pres.Close()
    Write-Host "PDF export completed successfully!"
}
catch {
    Write-Host "Error during export: $_"
}
finally {
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
