import string
#########################################################################
## 2013-03-17, AA: Helpers para nao encher as actions com tralha
#########################################################################

def handle_associate_outdoor_spot_post(req, logger):
    # TODO1: 2013-02-09
    # Diferenca entre assoc_before.split(';')
    # e os assspot com value = true -> os que sobrarem
    # devem ser apagados da outdoors_spots_db
    spots_to_delete = []
    spots_to_maintain = []
    new_spots_to_associate = []
    for input_control in req.post_vars:
        # se for uma checkbox dos spots associados previamente
        if 'assspot' in input_control:
            spots_to_maintain.append(input_control.replace('assspot_', ''))
        # se for uma checkbox dos spots new
        if 'newspot' in input_control:
            new_spots_to_associate.append(input_control.replace('newspot_', ''))
            # TODO2: 2013-02-09
            # input_control e uma checkbox
            # para aparecer aqui e porque estava a true
            # logo deve ser criado registo
            # em outdoors_spots_db
            #cbval = 'false'
            #if form.vars[input_control] != None:
                #cbval = 'true'
            #logger.debug('Valor da checkbox ' + input_control + ': ' + cbval)

    if req.vars.assoc_before != None:
        for prev_spot in req.vars.assoc_before.split(';'):
            if prev_spot not in spots_to_maintain:
                # deve ser apagado
                spots_to_delete.append(prev_spot)
        logger.debug('assoc_before *hidden*: ' + req.vars.assoc_before)

    logger.debug('Para manter: ' + string.join(spots_to_maintain, ','))
    logger.debug('Para apagar: ' + string.join(spots_to_delete, ','))
    logger.debug('Para associar (novos): ' + \
            string.join(new_spots_to_associate, ','))
