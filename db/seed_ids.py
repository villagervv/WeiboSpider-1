from sqlalchemy import text
from db.basic_db import db_session
from db.models import SeedIds


def get_seed_ids():
    return db_session.query(SeedIds.uid).filter(text('is_crawled=0')).all()


def set_seed_crawled(uid, result):
    """
    该表适用于用户抓取相关逻辑
    :param uid: 被抓取用户id
    :param result: 抓取结果
    :return: None
    """
    seed = db_session.query(SeedIds).filter(SeedIds.uid == uid).first()
    if seed:
        if seed.is_crawled == 0:
            seed.is_crawled = result
    else:
        seed = SeedIds(uid=uid, is_crawled=result)
        db_session.add(seed)
    db_session.commit()


def get_seed_by_id(uid):
    return db_session.query(SeedIds).filter(SeedIds.uid == uid).first()


def insert_seeds(ids):
    # 批量插入，遇到重复则跳过
    db_session.execute(SeedIds.__table__.insert().prefix_with('IGNORE'), [{'uid': i} for i in ids])
    db_session.commit()


def set_seed_other_crawled(uid):
    """
    存在则更新，不存在则插入
    :param uid: 用户id
    :return: None
    """
    seed = get_seed_by_id(uid)
    if seed is None:
        seed = SeedIds(uid=uid, is_crawled=1, other_crawled=1)
        db_session.add(seed)
    else:
        seed.other_crawled = 1
    db_session.commit()
