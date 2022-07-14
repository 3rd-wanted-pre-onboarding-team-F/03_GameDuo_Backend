from django.core.cache import cache

class RankingDataService(object):
    
    def get_ranking_data():
        ranking_list = []
        ranking_dict = cache.get('ranking_dict')
        rank = 1
        for score_key in ranking_dict.keys():
            for user in ranking_dict[score_key]:
                ranking_list.append({
                    'ranking':rank,
                    'userId': user,
                    'totalScore':score_key
                })
            rank += len(ranking_dict[score_key])
                
        return ranking_list
    
    def get_user_ranking_data(user_id):
        ranking_dict = cache.get('ranking_dict')
        user_id = int(user_id)
        user_ranking = {}
        rank = 1
        
        for score_key in ranking_dict.keys():
            if user_id in ranking_dict[score_key]:
                user_ranking['ranking'] = rank
                user_ranking['userId'] = user_id
                user_ranking['totalScore'] = score_key
                break
            rank += len(ranking_dict[score_key])
        
        return user_ranking
    
    def set_user_ranking_data(user_id, new_total_score):
        ranking_dict = cache.get('ranking_dict')
        for score_key in ranking_dict.keys():
            if user_id in ranking_dict[score_key]:
                ranking_dict[score_key].remove(user_id)
                break
        ranking_dict[new_total_score].add(user_id)
        cache.set('ranking_dict', ranking_dict, timeout=None)