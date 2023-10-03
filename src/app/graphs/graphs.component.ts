import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

@Component({
  selector: 'app-graphs',
  templateUrl: './graphs.component.html',
  styleUrls: ['./graphs.component.css']
})
export class GraphsComponent implements OnInit {
  actualImage: string = '';
  forecastImage: string = '';
  trainingImage: string = '';
  openPowerBI() {
    window.open('https://app.powerbi.com/groups/me/reports/ccaab1b7-6f33-4512-a92a-8e9e5267d1be/ReportSection', '_blank');
  }

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.actualImage = params['actualImage'] ;
      this.forecastImage = params['forecastImage'] ;
      this.trainingImage = params['trainingImage'] ;
    });
  }
}
