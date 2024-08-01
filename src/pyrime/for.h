/**
 * http://feng.zone/2017/05/21/%E5%AE%8F%E5%AE%9A%E4%B9%89%E9%BB%91%E9%AD%94%E6%B3%95-%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%A5%87%E6%8A%80%E6%B7%AB%E5%B7%A7-5/
 */
#ifndef FOR_H
#define FOR_H 1

#define PRIMITIVE_CAT(a, ...) a##__VA_ARGS__
#define CAT(a, ...) PRIMITIVE_CAT(a, __VA_ARGS__)

#define GET_SEC(x, n, ...) n
#define CHECK(...) GET_SEC(__VA_ARGS__, 0)
#define PROBE(x) x, 1
#define IS_EMPTY_0 PROBE()
#define IS_EMPTY(x, ...) CHECK(CAT(PRIMITIVE_CAT(IS_EMPTY_, x), 0))

#define EMPTY()
#define DEFER(id) id EMPTY()

#define FOR_EACH(macro, x, ...)                                                \
  CAT(FOR_EACH_, IS_EMPTY(__VA_ARGS__))(macro, x, __VA_ARGS__)
#define FOR_EACH_0(macro, x, ...)                                              \
  macro(x) DEFER(FOR_EACH_I)()(macro, __VA_ARGS__)
#define FOR_EACH_1(macro, x, ...) macro(x)
#define FOR_EACH_I() FOR_EACH

#define EVAL5(...) __VA_ARGS__
#define EVAL4(...) EVAL5(EVAL5(EVAL5(__VA_ARGS__)))
#define EVAL3(...) EVAL4(EVAL4(EVAL4(__VA_ARGS__)))
#define EVAL2(...) EVAL3(EVAL3(EVAL3(__VA_ARGS__)))
#define EVAL1(...) EVAL2(EVAL2(EVAL2(__VA_ARGS__)))
#define EVAL(...) EVAL1(EVAL1(EVAL1(__VA_ARGS__)))
#define FOR(...) EVAL(FOR_EACH(__VA_ARGS__))

#endif /* FOR.h */
