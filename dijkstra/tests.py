import timeit

from django.test import TestCase

from .models import Endpoint, LogisticNetwork


class EndpointTestCase(TestCase):
    # Desabilitado o setUp (linha 2 o comando de pass),
    # pois é realizado o teste de inserção durante o teste de Stress
    # abaixo
    def setUp(self):
        pass
        for aux in range(100):
            Endpoint.objects.create(name='Testing endpoint insertion nro ' + str(aux))

    def test_stress_insert_endpoint(self):
        insert_huge_amount = 10
        start_time = timeit.timeit(str(self.insert_huge_amount(insert_huge_amount)), number=100)
        print("tempo de execução de " + str(insert_huge_amount * 100) + " endpoints: {} segundos".format(start_time))

    def test_insert(self):
        aux = Endpoint.objects.create(name='A random name')
        self.assertTrue(isinstance(aux, Endpoint))
        self.assertEqual(aux.name, 'A random name')

    @classmethod
    def insert_huge_amount(self, quantity):
        for aux in range(quantity):
            Endpoint.objects.create(name='Testing Endpoint ' + str(aux))


class LogisticNetworkTestCase(TestCase):
    def setUp(self):
        print("Criando grafos dinamicamente, leva mais de 30 segundos, por favor, aguarde...")
        for networks in range(1):
            for aux in range(10):
                Endpoint.objects.create(name='Testing endpoint nro ' + str(aux))
            else:
                endpoints = Endpoint.objects.filter(name__contains='Testing endpoint nro').all()
                for endpoint in endpoints:
                    for endpoint_reverse in endpoints.reverse():
                        LogisticNetwork.objects.create(
                            origin=endpoint,
                            destiny=endpoint_reverse,
                            distance=int(endpoint.id) + int(endpoint_reverse.id)
                        )
            print("Grafo posição {} Criado com sucesso".format(networks))

    def test_list_networks(self):
        logistic_networks = LogisticNetwork.objects.all()
        self.assertEqual(logistic_networks.count(), 1)

