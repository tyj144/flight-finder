from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic import TemplateView
from finder.forms import IndexForm
from . import wikiAPI
from . import randomflight
import os
import pickle
import re

with open(os.path.dirname(os.path.realpath(__file__)) + "/airport_codes.pickle", "rb") as f:
	airport_codes = pickle.load(f)

# Create your views here.
class IndexView(TemplateView):
	template_name = 'index.html'

	def get(self, request):
		form = IndexForm()
		return render(request, self.template_name, { 'form': form })

	def post(self, request):
		form = IndexForm(request.POST)
		if form.is_valid():
			start_loc = form.cleaned_data['start_loc'].upper()
			start_date = form.cleaned_data['start_date']
			end_date = form.cleaned_data['end_date']
			# form.cleaned_data contains 'start_loc', 'start_date', 'end_date'
			
			flight_finder_response = randomflight.flight_finder(start_loc, start_date, end_date)

			if flight_finder_response == None:
				return render(request, self.template_name, { 'flight_not_found': True, 'form': form })
			else:
				depart, arrival = flight_finder_response
				
				# get the summary of the destination city
				#summary = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''
				#img_url = "something"
				summary = wikiAPI.get_summary(arrival[0])
				summary = ' '.join(re.split(r'(?<=[.:;])\s', summary)[:8])
				img_url = wikiAPI.get_img_url(arrival[0])

				# get the name of the city
				depart_name = airport_codes[depart[0]]
				arrival_name = airport_codes[arrival[0]]

				args = { 'form': form, 'depart': depart, 'arrival': arrival, 'summary': summary, 'img_url': img_url, 
					'depart_name': depart_name, 'arrival_name': arrival_name, 
					**form.cleaned_data}
				return render(request, 'flight.html', args)
		else:
			return render(request, self.template_name, { 'form': form })