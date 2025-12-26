fetch(`/analytics/owner-dashboard/?clinic=${CLINIC_ID}`)
  .then(res => res.json())
  .then(data => {
    console.log("Dashboard data:", data);

    // ===== KPIs =====
    document.getElementById("kpi-earnings").innerText = "₹" + data.total_earnings;
    document.getElementById("kpi-new").innerText = data.new_vs_repeat.new;
    document.getElementById("kpi-repeat").innerText = data.new_vs_repeat.repeat;
    document.getElementById("kpi-growth").innerText =
      data.visit_growth_pct ? data.visit_growth_pct + "%" : "N/A";
    document.getElementById("kpi-profit").innerText = "₹" + data.net_profit;

    // ===== GET CANVAS ELEMENTS (THIS WAS MISSING) =====
    const patientsPerDayEl = document.getElementById('patientsPerDay');
    const newRepeatEl = document.getElementById('newRepeat');
    const busiestHoursEl = document.getElementById('busiestHours');
    const doctorRevenueEl = document.getElementById('doctorRevenue');
    const paymentMethodsEl = document.getElementById('paymentMethods');
    const doctorMarginEl = document.getElementById('doctorMargin');

    // ===== CHARTS =====

    new Chart(patientsPerDayEl, {
      type: 'line',
      data: {
        labels: data.patients_per_day.map(d => d.day),
        datasets: [{
          label: 'Patients per day',
          data: data.patients_per_day.map(d => d.count)
        }]
      }
    });

    new Chart(newRepeatEl, {
      type: 'doughnut',
      data: {
        labels: ['New', 'Repeat'],
        datasets: [{
          data: [data.new_vs_repeat.new, data.new_vs_repeat.repeat]
        }]
      }
    });

    new Chart(busiestHoursEl, {
      type: 'bar',
      data: {
        labels: data.busiest_hours.map(h => h.hour),
        datasets: [{
          label: 'Visits',
          data: data.busiest_hours.map(h => h.count)
        }]
      }
    });

    new Chart(doctorRevenueEl, {
      type: 'bar',
      data: {
        labels: data.doctor_wise_revenue.map(d => d.doctor__user__username),
        datasets: [{
          label: 'Revenue',
          data: data.doctor_wise_revenue.map(d => d.total)
        }]
      }
    });

    new Chart(paymentMethodsEl, {
      type: 'doughnut',
      data: {
        labels: data.payment_methods.map(p => p.payment_method),
        datasets: [{
          data: data.payment_methods.map(p => p.total)
        }]
      }
    });

    new Chart(doctorMarginEl, {
      type: 'bar',
      data: {
        labels: data.doctor_margins.map(d => d.doctor),
        datasets: [
          {
            label: 'Revenue',
            data: data.doctor_margins.map(d => d.revenue)
          },
          {
            label: 'Salary Paid',
            data: data.doctor_margins.map(d => d.payout)
          }
        ]
      }
    });
});
