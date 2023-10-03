import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GraphsService {

  constructor(private http: HttpClient) { }

  generateGraphs(formData: FormData): Observable<any> {
    return this.http.post<any>('http://localhost:5000/sales-forecast', formData);
  }
  openPowerBI() {
    window.open('https://app.powerbi.com/groups/me/reports/ccaab1b7-6f33-4512-a92a-8e9e5267d1be/ReportSection', '_blank');
  }
}
