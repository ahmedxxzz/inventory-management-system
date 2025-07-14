from model.Factory_compnents_model.report_model import ReportModel



class ReportController:
    def __init__(self, buys_operations,operation_type='buy'):
        self.buys_operations = buys_operations
        '''
        buys = [{'facname': 'facname','productcode': 'productcode','price': 0,'quantity': 0,'discount': 0,'supplier': 'golden rose','paid': 'paid or not',},{'facname': 'facname','productcode': 'productcode','price': 0,'quantity': 0,'discount': 0,'supplier': 'golden rose','paid': 'paid or not',},]
        payes = ['facname', amount of money, 'safe_type']
        returns = ['facname', product code, quantity, reason]
        '''
        print('here is report controller')