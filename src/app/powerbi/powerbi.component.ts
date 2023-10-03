import { Component } from '@angular/core';

@Component({
  selector: 'app-powerbi',
  templateUrl: './powerbi.component.html',
  styleUrls: ['./powerbi.component.css']
})
export class PowerbiComponent {
  openPowerBIReport() {
    const powerBIReportUrl = 'https://app.powerbi.com/groups/me/reports/ccaab1b7-6f33-4512-a92a-8e9e5267d1be/ReportSection';
    window.open(powerBIReportUrl, '_blank');
  }
}