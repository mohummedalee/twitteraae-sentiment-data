# -*- coding: utf-8 -*-
import logging

import click

from data_utils import get_attr_sentiments, get_data, get_race, \
    mention_split, to_file, to_file_raw
from twitter_utils import happy, sad

MIN_SENTENCE_LEN = 3


@click.command()
@click.argument('input_file_path', type=click.Path(exists=True))
@click.argument('output_dir_raw_path', type=click.Path())
@click.argument('output_dir_path', type=click.Path())
@click.argument('main_task')
@click.argument('protect_att')
def main(input_file_path, output_dir_path, output_dir_raw_path, main_task, protect_att):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    df = get_data(input_file_path)

    logger.info('read all tweets and removed duplicates')

    if main_task == 'sentiment':
        if protect_att == 'race':
            logger.info('making sentiment-race')
            # AAVE sentences that are `happy`
            pos_pos = get_attr_sentiments(df, happy, sad, 'aa', MIN_SENTENCE_LEN)
            # SAE sentences that are `happy`
            pos_neg = get_attr_sentiments(df, happy, sad, 'wh', MIN_SENTENCE_LEN)
            # AAVE sentences that are `sad`
            neg_pos = get_attr_sentiments(df, sad, happy, 'aa', MIN_SENTENCE_LEN)
            # SAE sentences that are `sad`
            neg_neg = get_attr_sentiments(df, sad, happy, 'wh', MIN_SENTENCE_LEN)
        else:
            logger.error('not supporting this task...')
            exit(-1)
    elif main_task == 'mention':
        if protect_att == 'race':
            logger.info('making mention-race')
            wh, aa = get_race(df, MIN_SENTENCE_LEN)
            pos_pos, neg_pos = mention_split(aa, MIN_SENTENCE_LEN)
            pos_neg, neg_neg = mention_split(wh, MIN_SENTENCE_LEN)
        else:
            logger.error('not supporting this task...')
            exit(-1)
    else:
        logger.error('not supporting this task...')
        exit(-1)

    logger.info('done collecting data')

    # size = 100000
    # sentences = pos_pos[:size] + pos_neg[:size] + neg_pos[:size] + neg_neg[:size]
    # write all sentences -- don't cut at a size
    sentences = pos_pos + pos_neg + neg_pos + neg_neg
    logger.info('building vocab...')
    vocab = list(set([item for sublist in sentences for item in sublist]))
    id2voc = dict(enumerate(vocab))
    voc2id = {v: k for k, v in id2voc.iteritems()}

    logger.info('writing untokenized (raw) sentences to ' + output_dir_raw_path)
    to_file_raw(output_dir_raw_path, pos_pos, pos_neg, neg_pos, neg_neg)
    # to_file(output_dir_path, voc2id, vocab, pos_pos[:size], pos_neg[:size], neg_pos[:size], neg_neg[:size])
    logger.info('writing tokenized (processed) sentences to ' + output_dir_path)
    to_file(output_dir_path, voc2id, vocab, pos_pos, pos_neg, neg_pos, neg_neg)
    logger.info('written to file. exiting.')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
