import csv
from rest_framework import status
from rest_framework.response import Response
from .serializers import CSVRowSerializer
from .models import CSVRow

class UploadCSVView():
    
    def post(self, request):
        file = request.FILES.get('file')
        if not file.name.endswith('.csv'):
            return Response({'error': 'File is not a CSV'}, status=status.HTTP_400_BAD_REQUEST)
        rows = csv.reader(file.read().decode('utf-8').splitlines())
        next(rows)  # skip header row
        for row in rows:
            serializer = CSVRowSerializer(data={'column1': row[0], 'column2': row[1], 'column3': row[2]})
            if serializer.is_valid():
                serializer.save()
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)







class GetTop50View():

    def get(self, request):
        column_name = request.query_params.get('column_name')
        sort_order = request.query_params.get('sort_order')
        if column_name not in ['column1', 'column2', 'column3']:
            return Response({'error': 'Invalid column name'}, status=status.HTTP_400_BAD_REQUEST)
        if sort_order not in ['asc', 'desc']:
            return Response({'error': 'Invalid sort order'}, status=status.HTTP_400_BAD_REQUEST)
        qs = CSVRow.objects.order_by(f'{sort_order}{column_name}')[:50]
        serializer = CSVRowSerializer(qs, many=True)
        return Response(serializer.data)