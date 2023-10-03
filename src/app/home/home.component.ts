import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  fileToUpload: File | null = null;
  periodicity: string = 'weekly';
  periodicityNumber: number = 1;

  constructor(private http: HttpClient, private router: Router) {}

  onFileSelected(event: any) {
    this.fileToUpload = event.target.files[0];
  }

  submitForm() {
    if (this.fileToUpload) {
      const formData: FormData = new FormData();
      formData.append('file', this.fileToUpload);
      formData.append('periodicity', this.periodicity);
      formData.append('periodicityNumber', this.periodicityNumber.toString());

      this.http.post('http://localhost:5000/sales-forecast', formData)
        .subscribe(
          (response: any) => {
            console.log('Form submitted successfully!', response);
            const queryParams = {
              actualImage: 'data:image/png;base64,' + response.actualImage,
              forecastImage: 'data:image/png;base64,' + response.forecastImage,
              trainingImage: 'data:image/png;base64,' + response.trainingImage
            };
            this.router.navigate(['/graphs'], { queryParams });
          },
          error => {
            console.error('Error submitting form:', error);
            // Handle error response
          }
        );
    }
  }
}
